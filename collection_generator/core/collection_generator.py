"""
Collection Generator
--------------------

The collection generator inherits from ``asset_scanner.core.BaseExtractor``
It provides the workflow for what to do when ``process_file`` is called.

The collection generator is an aggregator. It is designed to take the content
from the items and generate a summary of the items in each collection.

"""

__author__ = """Richard Smith"""
__contact__ = 'richard.d.smith@stfc.ac.uk'
__copyright__ = "Copyright 2020 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"


from asset_scanner.core import BaseExtractor
from asset_scanner.core.utils import dict_merge

import logging

LOGGER = logging.getLogger(__name__)


class CollectionGenerator(BaseExtractor):
    """
    Class to handle the generation of collections
    through aggregating content from STAC items.
    """

    PROCESSOR_ENTRY_POINT = 'collection_generator.processors'

    def _load_processor(self) -> 'BaseProcessor':
        """
        Extract the required information from the configuration file
        and load the processor
        """

        aggregator_conf = self.conf['collection_aggregator']
        name = aggregator_conf['name']
        processor_kwargs = aggregator_conf['inputs']

        return self.processors.get_processor(name, **processor_kwargs)

    def run_processors(self, collection_id: str, description: 'ItemDescription') -> dict:
        """
        Run the configured processor
        :param collection_id: id of collection to generate a summary for
        :param description: An ItemDescription object containing the metadata about the collection.

        :return: Output from the processor
        """

        processor = self._load_processor()

        metadata = processor.run(collection_id, description)

        return metadata

    def process_file(self, filepath: str, source_media: str = 'POSIX', **kwargs) -> None:
        """
        Run the workflow

        :param filepath: File path related to the collection. Only used to get
        the correct description file.
        :param source_media: Unused. Present to match signature of abstract parent.
        :param kwargs: Unused. Present to match signature of abstract parent.
        """

        LOGGER.info(f'Processing: {filepath}')

        # Get description file
        description = self.item_descriptions.get_description(filepath)

        # Get collection id
        collection_id = description.collections.id
        LOGGER.info(f'Collection ID: {collection_id}')

        # Only expects a single processor
        processor_output = self.run_processors(collection_id, description)

        # Check collection description has extent and description fields before output.
        if not all(key in processor_output for key in ('extent', 'description')):
            return

        # Base collection
        base_collection_dict = {
            'type': 'Collection',
            'license': 'default'
        }

        # Merge the output from the processor into the base
        body = dict_merge(base_collection_dict, processor_output)

        # Prepare the output
        output = {
            'id': collection_id,
            'body': body
        }

        self.output(filepath, source_media, output)



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

from typing import Dict

from asset_scanner.core import BaseExtractor
from asset_scanner.core.utils import dict_merge
from asset_scanner.types.source_media import StorageType


import logging

LOGGER = logging.getLogger(__name__)


class CollectionGenerator(BaseExtractor):
    """
    Class to handle the generation of collections
    through aggregating content from STAC items.
    """

    PROCESSOR_ENTRY_POINT = 'asset_scanner.processors'


    def run_processors(self,
                       filepath: str,
                       description: 'ItemDescription',
                       source_media: StorageType,
                       **kwargs: Dict) -> Dict:
        """
        Extract additional information based on processors listed in the collections
        section of the item-descriptions.

        :param filepath: path of file being processed
        :param description: An ItemDescription object containing the metadata about the collection.
        :param source_media: Source Media Type
        """

        # Get defaults
        tags = description.collections.defaults

        # Execute the extraction functions
        processors = description.collections.extraction_methods

        for processor in processors:
            metadata = self._run_facet_processor(processor, filepath, source_media)

            # Merge the extract metadata with that already retrieved
            if metadata:
                tags = dict_merge(tags, metadata)

        # Process multi-values

        # Apply mappings

        # Apply overrides

        return tags

    def get_summaries(self, collection_id: str, description: 'ItemDescription') -> Dict:
        """
        Summarise the content in the item data table to generate collections. This will
        get the queryables and spatial/temporal extent based on indexed data.

        :param collection_id:
        :param description:
        :return:
        """

        # Get defaults
        tags = description.collections.defaults

        # Execute the extraction functions
        processors = description.collections.extraction_methods

        for processor in processors:
            metadata = self._run_facet_processor(processor, filepath, source_media)

            # Merge the extract metadata with that already retrieved
            if metadata:
                tags = dict_merge(tags, metadata)

        # Process multi-values

        # Apply mappings

        # Apply overrides

        return tags

    def get_summaries(self, collection_id: str, description: 'ItemDescription') -> Dict:
        """
        Summarise the content in the item data table to generate collections. This will
        get the queryables and spatial/temporal extent based on indexed data.

        :param collection_id:
        :param description:
        :return:
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

        # Get summaries
        summaries = self.get_summaries(collection_id, description)

        # Run processors to extract additional information
        processor_output = self.run_processors(filepath, description, source_media)

        # Check collection description has extent and description fields before output.
        if not all(key in processor_output for key in ('extent', 'description')):
            return

        # Base collection
        base_collection_dict = {
            'type': 'Collection',
            'license': 'default'
        }

        # Merge the output from the processors into the base
        body = dict_merge(base_collection_dict, processor_output)

        # Merge the aggregations into the body. We do it in this order
        # so that default extents can be provided in the collections description.
        body = dict_merge(body, summaries)

        # Prepare the output
        output = {
            'id': collection_id,
            'body': body
        }

        self.output(filepath, source_media, output)



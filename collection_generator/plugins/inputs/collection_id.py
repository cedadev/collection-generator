# encoding: utf-8
"""

"""
__author__ = 'Richard Smith'
__date__ = '25 Aug 2021'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'


import yaml

from asset_scanner.plugins.input_plugins.base import BaseInputPlugin
from asset_scanner.core.utils import load_description_files

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from asset_scanner.core import BaseExtractor


class CollectionIDInputPlugin(BaseInputPlugin):

    def __init__(self, **kwargs):
        self.description_root = kwargs['description_root']

    def run(self, extractor: 'BaseExtractor') -> None:

        file_list = load_description_files(self.description_root)

        for file in file_list:

            with open(file) as reader:
                data = yaml.safe_load(reader)

                if data.get('collection', {}).get('id'):
                    collection_path = data.get('datasets')[0]
                    extractor.process_file(collection_path)
                else:
                    continue



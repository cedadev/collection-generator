# encoding: utf-8
"""

"""
__author__ = 'Richard Smith'
__date__ = '25 Aug 2021'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'


from asset_scanner.core.processor import BaseProcessor
import abc


class BaseAggregationProcessor(BaseProcessor):
    """
    Modify the run method signature as the aggregation processor requires
    different information.
    """

    @abc.abstractmethod
    def run(self, collection_id: str, description: 'ItemDescription') -> dict:
        ...

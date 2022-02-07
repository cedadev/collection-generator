from asset_scanner.core.processor import BaseAggregationProcessor
from asset_scanner.core.types import SpatialExtent, TemporalExtent

import json
import os

from typing import Optional, List, Dict

from numpy import empty

class JSONAggregator(BaseAggregationProcessor):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.filepath = kwargs['filepath']

    def get_facet_values(self, facet: str, file_id: str) -> List:

        facet_values = []

        with open(self.filepath, 'r') as file:
            file_data = json.load(file)

            for item in file_data:
                if item['body']['collection_id'] == file_id:
                    values = item['body']['properties'][facet]
                    if isinstance(values, list):
                        facet_values.extend(values)
                    else:
                        facet_values.append(values)
        return list(set(facet_values))

    @staticmethod
    def get_spatial_extent(item_list: list) -> Optional[SpatialExtent]:
        ...

    @staticmethod
    def get_temporal_extent(item_list: list) -> Optional[TemporalExtent]:
        start_datetime = []
        end_datetime = []
        datetime = []

        for item in item_list:
            start_datetime.append(item['properties'].get('start_datetime'))
            end_datetime.append(item['properties'].get('end_datetime'))
            datetime.append(item['properties'].get('datetime'))

        start_datetime = list(set(start_datetime))
        end_datetime = list(set(end_datetime))
        datetime = list(set(datetime))



    def get_extent(self, file_id: str) -> Dict:
        item_list = []
        with open(self.filepath, 'r') as file:
            file_data = json.load(file)

            for item in file_data:
                if item['body']['collection_id'] ==  file_id:
                    item_list.append(item)

        spatial_extent = self.get_spatial_extent(item_list)
        temporal_extent = self.get_temporal_extent(item_list)
        

    def run(self, file_id: str, description: 'ItemDescription') -> dict:
        
        metadata = {}

        facets = set(description.facets.aggregation_facets + description.facets.search_facets)

        summaries = {}
        
        for facet in facets:
            values = self.get_facet_values(facet, file_id)
            if values:
                summaries[facet] = values

        metadata['summaries'] = summaries

        # No need to include extents since the example scanner has none.

        return metadata
        
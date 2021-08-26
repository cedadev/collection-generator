# encoding: utf-8
"""

"""
__author__ = 'Richard Smith'
__date__ = '26 Aug 2021'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

from typing import List, Union, Int, Float, Optional

Numeric = Union[Int, Float]
TemporalExtent = List[List[Optional[str]]]
SpatialExtent = List[List[Numeric]]

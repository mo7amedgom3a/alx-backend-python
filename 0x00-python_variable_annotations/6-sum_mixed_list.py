#!/usr/bin/env python3
"""Sum a mixed list
"""

from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """Return sum of list of mixed floats and ints
    """
    return sum(mxd_lst)

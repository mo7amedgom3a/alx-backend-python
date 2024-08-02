#!/usr/bin/env python3
"""Complex types - list of floats"""


from typing import Iterable, Tuple, Sequence, List


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """Returns a list of tuples containing the length of the elements"""
    return [(i, len(i)) for i in lst]

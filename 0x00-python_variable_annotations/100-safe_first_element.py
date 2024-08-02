#!/usr/bin/env python3
"""safe_first_element module"""


from typing import Sequence, Union, Any, TypeVar


def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    """Returns the first element of a list if it exists, otherwise None."""
    if lst:
        return lst[0]
    else:
        return None

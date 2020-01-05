"""
Person data object.
"""


from typing import NamedTuple
from typing import Optional


class Person(NamedTuple):
    """Person data object."""

    id_: int
    name: str
    gender: Optional[str] = None  # "M" or "F" or None
    father_id: Optional[int] = None
    mother_id: Optional[int] = None
    birth_order: Optional[int] = None
    spouse_id: Optional[int] = None


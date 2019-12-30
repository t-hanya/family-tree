"""
Person table object.
"""


from typing import Optional
from typing import Sequence
from typing import Tuple

from familytree.person import Person


class Table:
    """Person table object."""

    def __init__(self, persons: Sequence[Person]) -> None:
        self.persons = persons

    def get(self, person_id: int) -> Optional[Person]:
        """Get person by person id."""
        for person in self.persons:
            if person.id_ == person_id:
                return person

        raise KeyError(
            'Cannot get person with id = {}'.format(person_id))

    def get_parents(self,
                    person: Person
                    ) -> Tuple[Optional[Person], Optional[Person]]:
        """Get parents of the person."""
        fid = person.father_id
        mid = person.mother_id
        father = self.get(fid) if fid is not None else None
        mother = self.get(mid) if mid is not None else None
        return (father, mother)

    def get_spouse(self,
                   person: Person,
                  ) -> Optional[Person]:
        """Get spouse of the person."""
        if person.spouse_id is None:
            return None
        else:
            return self.get(person.spouse_id)

    def find_children(self,
                      father: Person,
                      mother: Person
                     ) -> Tuple[Person]:
        """Find children for the parents."""
        children = []
        for person in self.persons:
            if (person.father_id == father.id_ and
                person.mother_id == mother.id_):
                children.append(person)
        return tuple(children)


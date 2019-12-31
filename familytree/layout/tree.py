"""
Tree layout algorithm.
"""


from typing import List
from typing import Union

from familytree.person import Person
from familytree.table import Table
from familytree.element import PersonBox
from familytree.element import SpouseLink
from familytree.element import ParentChildLink


def _get_person_boxes(elements: list) -> list:
    return [e for e in elements if hasattr(e, 'person')]


class TreeLayout:
    """Tree layout algorithm."""

    def __init__(self,
                 person_box_class: type = PersonBox,
                 spouse_link_class: type = SpouseLink,
                 parent_child_link_class: type = ParentChildLink,
                 ) -> None:
        self.person_box_class = person_box_class
        self.spouse_link_class = spouse_link_class
        self.parent_child_link_class = parent_child_link_class

        # constants
        self.x_margin = person_box_class.width // 2
        self.y_margin = person_box_class.height // 4
        self.unit_w = person_box_class.width + self.x_margin * 2
        self.unit_h = person_box_class.height + self.y_margin * 2

    def __call__(self,
                 table: Table,
                 root: Person,
                 x0: int = 0,
                 y0: int = 0
                ) -> List[Union[PersonBox, SpouseLink, ParentChildLink]]:

        # handle single person
        spouse = table.get_spouse(root)
        if spouse is None:
            x = x0 + self.x_margin
            y = y0 + self.y_margin
            elements = [self.person_box_class(root, x, y)]
            return elements

        # get family members from the table
        if root.gender == 'M':
            parents = [root, spouse]
        else:
            parents = [spouse, root]
        children = table.find_children(*parents)
        children = sorted(children,
                          key=lambda p: (p.birth_order, p.id_))

        elements = []
        x = x0

        # elements for children
        for child in children:
            elems = self(table, child, x0=x, y0=y0 + self.unit_h)
            x = max([e.xmax for e in _get_person_boxes(elems)])
            x += self.x_margin
            elements += elems
        child_elements = [e for e in _get_person_boxes(elements)
                          if e.person in children]

        # elements for parents
        center = (x0 + x) // 2
        x = max(x0, center - self.unit_w)
        x1 = x + self.x_margin
        x2 = x + self.x_margin + self.unit_w
        y = y0 + self.y_margin
        elements.append(self.person_box_class(parents[0], x1, y))
        elements.append(self.person_box_class(parents[1], x2, y))

        # parent and child link
        ym = y0 + self.person_box_class.height // 2
        for child_elem in child_elements:
            x1 = x + self.unit_w
            y1 = ym
            x2 = (child_elem.xmin + child_elem.xmax) // 2
            y2 = child_elem.ymin
            elements.append(self.parent_child_link_class(x1, y1, x2, y2))

        # spouse link
        elements.append(self.spouse_link_class(
            x + self.unit_w - self.x_margin, ym,
            x + self.unit_w + self.x_margin, ym))

        return elements

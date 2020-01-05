"""
Butterfly layout alborithm.
"""


from typing import List
from typing import Union
from typing import Tuple

from familytree.person import Person
from familytree.table import Table
from familytree.element import PersonBox
from familytree.element import SpouseLink
from familytree.element import ParentChildLink
from familytree.layout.tree import TreeLayout


Element = Union[PersonBox, SpouseLink, ParentChildLink]


def _get_brothers_and_sisters(table, target) -> List[Person]:
    """Get brothers and sisters for the person."""
    parents = table.get_parents(target)
    if parents[0] is None or parents[1] is None:
        return []
    children = table.find_children(*parents)
    children = [c for c in children if c != target]
    children = sorted(children, key=lambda p: (p.birth_order, p.id_))
    return children


def _get_x_range(elements: List[Element]) -> Tuple[int, int]:
    """Get x value range of boxes in elements"""
    boxes = [e for e in elements if hasattr(e, 'person')]
    xmin = min([b.xmin for b in boxes])
    xmax = max([b.xmax for b in boxes])
    return (xmin, xmax)


def _get_box(elements: List[Element], person: Person) -> PersonBox:
    """Get person box for the person data."""
    for e in elements:
        if hasattr(e, 'person') and e.person == person:
            return e
    raise KeyError(
        'Cannot find person box with id = {}'.format(person.id_))


class ButterflyLayout:
    """Buttefly layout algorithm."""

    def __init__(self,
                 person_box_class: type = PersonBox,
                 spouse_link_class: type = SpouseLink,
                 parent_child_link_class: type = ParentChildLink,
                 ) -> None:
        self.person_box_class = person_box_class
        self.spouse_link_class = spouse_link_class
        self.parent_child_link_class = parent_child_link_class
        self.tree_layout_func = TreeLayout(
            person_box_class=person_box_class,
            spouse_link_class=spouse_link_class,
            parent_child_link_class=parent_child_link_class)

        # constants
        self.x_margin = person_box_class.width // 2
        self.y_margin = person_box_class.height // 4
        self.unit_w = person_box_class.width + self.x_margin * 2
        self.unit_h = person_box_class.height + self.y_margin * 2

    def _layout_children(self,
                         elements: List[Element],
                         x: int,
                         table: Table,
                         children: List[Person],
                        ) -> Tuple[List[Element], int]:
        for child in children:
            elems = self.tree_layout_func(
                table, child, x0=x, y0=self.unit_h)
            _, xmax = _get_x_range(elems)
            x = xmax + self.x_margin
            elements += elems
        return (elements, x)

    def _layout_parents(self,
                        elements: List[Element],
                        x: int,
                        table: Table,
                        parents: Tuple[Person],
                        children: List[Person]
                       ) -> Tuple[List[Element], int]:
        if parents[0] is None or parents[1] is None:
            return elements, x

        # parent boxes
        left = _get_box(elements, children[0]).xmin
        right = _get_box(elements, children[-1]).xmax
        center = (left + right) // 2
        x = max(x, center - self.unit_w)
        x1 = x + self.x_margin
        x2 = x + self.x_margin + self.unit_w
        y = self.y_margin

        elements.append(self.person_box_class(parents[0], x1, y))
        elements.append(self.person_box_class(parents[1], x2, y))

        # parent-child link
        ym = self.person_box_class.height // 2
        child_elements = [_get_box(elements, child)
                          for child in children]
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

        x = x + 2 * self.unit_w
        return (elements, x)

    def __call__(self,
                 table: Table,
                 target: Person) -> List[Element]:
        # a) single
        #   - with parent info -> tree(father)
        #   - no parent info -> tree(target)
        spouse = table.get_spouse(target)
        if spouse is None:
            parents = table.get_parents(target)
            if parents[0] and parents[1]:
                return self.tree_layout_func(table, parents[0])
            else:
                return self.tree_layout_func(table, target)

        if target.gender == 'M':
            husband = target
            wife = spouse
        else:
            husband = spouse
            wife = target

        parents1 = table.get_parents(husband)
        parents2 = table.get_parents(wife)

        # b) couple, no parents info -> tree(target)
        if ((parents1[0] is None or parents1[1] is None) and
            (parents2[0] is None or parents2[1] is None)):
            return self.tree_layout_func(table, target)

        # c) couple, with parents info -> butterfly layout
        children1 = _get_brothers_and_sisters(table, husband)
        children2 = _get_brothers_and_sisters(table, wife)

        elements = []

        # layout children
        x = 0
        elements, x = self._layout_children(elements, x, table, children1)
        elements, x = self._layout_children(elements, x, table, [husband])
        elements, x = self._layout_children(elements, x, table, children2)

        # layout parents
        x = 0
        elements, x = self._layout_parents(
            elements, x, table, parents1, children1 + [husband])
        elements, x = self._layout_parents(
            elements, x, table, parents2, [wife] + children2)

        return elements

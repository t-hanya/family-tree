"""
Unittest for familytree.layout.tree module.
"""


from familytree.person import Person
from familytree.table import Table
from familytree.layout.tree import TreeLayout


def _get_box(elements, person):
    filtered = [e for e in elements
                if getattr(e, 'person', None) == person]
    assert len(filtered) == 1
    return filtered[0]


class TestTreeLayout:

    def test_tree(self):
        persons = [
            Person(1, "Father", gender="M", spouse_id=2),
            Person(2, "Mother", gender="F", spouse_id=1),
            Person(3, "Child1", father_id=1, mother_id=2, birth_order=1),
            Person(4, "Child2", father_id=1, mother_id=2, birth_order=2),
            Person(5, "Child3", father_id=1, mother_id=2, birth_order=3),
        ]
        layout_func = TreeLayout()
        elements = layout_func(Table(persons), persons[0])

        assert len(elements) == 5 + 1 + 3

        box_p1 = _get_box(elements, persons[0])
        box_p2 = _get_box(elements, persons[1])
        box_p3 = _get_box(elements, persons[2])
        box_p4 = _get_box(elements, persons[3])
        box_p5 = _get_box(elements, persons[4])

        assert box_p1.xmin < box_p2.xmin
        assert box_p1.ymin == box_p2.ymin

        assert box_p3.xmin < box_p4.xmin < box_p5.xmin
        assert box_p3.ymin == box_p4.ymin == box_p5.ymin

    def test_single(self):
        persons = [
            Person(1, "Name1"),
            Person(2, "Name2")
        ]
        layout_func = TreeLayout()
        elements = layout_func(Table(persons), persons[0])
        assert len(elements) == 1

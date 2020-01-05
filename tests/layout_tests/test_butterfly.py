"""
Unittest for familytree.layout.butterfly module.
"""


from familytree.person import Person
from familytree.table import Table
from familytree.layout.butterfly import ButterflyLayout


def _get_box(elements, person):
    filtered = [e for e in elements
                if getattr(e, 'person', None) == person]
    assert len(filtered) == 1
    return filtered[0]


class TestButterflyLayout:

    def test_butterfly(self):
        table = Table([
            Person(1, "father1", "M", spouse_id=2),
            Person(2, "mother1", "F", spouse_id=1),
            Person(3, "brother1", "M", father_id=1, mother_id=2, birth_order=1),
            Person(4, "brother2", "M", father_id=1, mother_id=2, birth_order=3),

            Person(5, "husband", "M", spouse_id=6, father_id=1, mother_id=2, birth_order=2),
            Person(6, "wife", "F", spouse_id=5, father_id=7, mother_id=8, birth_order=1),

            Person(7, "father2", "M", spouse_id=8),
            Person(8, "mother2", "F", spouse_id=7),
            Person(9, "sister1", "F", father_id=7, mother_id=8, birth_order=2)
        ])
        layout_func = ButterflyLayout()
        elements = layout_func(table, table.get(5))
        assert len(elements) == 9 + 3 + 5

        box_p1 = _get_box(elements, table.get(1))
        box_p2 = _get_box(elements, table.get(2))
        box_p3 = _get_box(elements, table.get(3))
        box_p4 = _get_box(elements, table.get(4))
        box_p5 = _get_box(elements, table.get(5))
        box_p6 = _get_box(elements, table.get(6))
        box_p7 = _get_box(elements, table.get(7))
        box_p8 = _get_box(elements, table.get(8))
        box_p9 = _get_box(elements, table.get(9))

        assert box_p1.xmin < box_p2.xmin < box_p7.xmin < box_p8.xmin
        assert box_p1.ymin == box_p2.ymin == box_p7.ymin == box_p8.ymin

        assert box_p3.xmin < box_p4.xmin < box_p5.xmin < box_p6.xmin < box_p9.xmin
        assert box_p3.ymin == box_p4.ymin == box_p5.ymin == box_p6.ymin == box_p9.ymin

    def test_single_no_parent_info(self):
        table = Table([
            Person(1, "target"),
            Person(2, "other"),
            Person(3, "other"),
        ])
        layout_func = ButterflyLayout()
        elements = layout_func(table, table.get(1))
        assert len(elements) == 1

    def test_single_with_parents(self):
        table = Table([
            Person(1, "father", "M", spouse_id=2),
            Person(2, "mother", "F", spouse_id=1),
            Person(3, "target", "M", father_id=1, mother_id=2, birth_order=1),
            Person(4, "brother", "M", father_id=1, mother_id=2, birth_order=2),
        ])
        layout_func = ButterflyLayout()
        elements = layout_func(table, table.get(3))
        assert len(elements) == 4 + 1 + 2

        box_p1 = _get_box(elements, table.get(1))
        box_p2 = _get_box(elements, table.get(2))
        box_p3 = _get_box(elements, table.get(3))
        box_p4 = _get_box(elements, table.get(4))

        assert box_p1.xmin < box_p2.xmin
        assert box_p1.ymin == box_p2.ymin

        assert box_p3.xmin < box_p4.xmin
        assert box_p3.ymin == box_p4.ymin

    def test_couple_no_parent_info(self):
        table = Table([
            Person(1, "husband", "M", spouse_id=2),
            Person(2, "wife", "F", spouse_id=1),
        ])
        layout_func = ButterflyLayout()
        elements = layout_func(table, table.get(1))
        assert len(elements) == 2 + 1

        box_p1 = _get_box(elements, table.get(1))
        box_p2 = _get_box(elements, table.get(2))

        assert box_p1.xmin < box_p2.xmin
        assert box_p1.ymin == box_p2.ymin

    def test_couple_partial_parent_info(self):
        table = Table([
            Person(1, "father1", "M", spouse_id=2),
            Person(2, "mother1", "F", spouse_id=1),
            Person(3, "brother1", "M", father_id=1, mother_id=2, birth_order=1),
            Person(4, "brother2", "M", father_id=1, mother_id=2, birth_order=3),

            Person(5, "husband", "M", spouse_id=6, father_id=1, mother_id=2, birth_order=2),
            Person(6, "wife", "F", spouse_id=5),
        ])
        layout_func = ButterflyLayout()
        elements = layout_func(table, table.get(5))
        assert len(elements) == 6 + 2 + 3

        box_p1 = _get_box(elements, table.get(1))
        box_p2 = _get_box(elements, table.get(2))
        box_p3 = _get_box(elements, table.get(3))
        box_p4 = _get_box(elements, table.get(4))
        box_p5 = _get_box(elements, table.get(5))
        box_p6 = _get_box(elements, table.get(6))

        assert box_p1.xmin < box_p2.xmin
        assert box_p1.ymin == box_p2.ymin

        assert box_p3.xmin < box_p4.xmin < box_p5.xmin < box_p6.xmin
        assert box_p3.ymin == box_p4.ymin == box_p5.ymin == box_p6.ymin

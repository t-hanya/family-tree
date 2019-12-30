"""
Unittest for familytree.table module.
"""


import pytest

from familytree.person import Person
from familytree.table import Table


class TestTable:
    # get_spouse
    # get_children
    # iteration

    def test_get(self):
        table = Table([Person(1, "Name1"), Person(2, "Name2")])
        p = table.get(2)
        assert p.id_ == 2
        assert p.name == "Name2"

    def test_get_key_error(self):
        table = Table([Person(1, "Name")])
        with pytest.raises(KeyError):
            table.get(2)

    def test_get_parents(self):
        father = Person(1, "Father")
        mother = Person(2, "Mother")
        child = Person(3, "Child", father_id=1, mother_id=2)
        table = Table([father, mother, child])
        parents = table.get_parents(child)
        assert len(parents) == 2
        assert parents[0] == father
        assert parents[1] == mother

    def test_get_parents_no_result(self):
        child = Person(1, "Name")
        table = Table([child])
        parents = table.get_parents(child)
        assert len(parents) == 2
        assert parents[0] == None
        assert parents[1] == None

    def test_get_parents_key_error(self):
        child = Person(1, "Child", father_id=999)
        table = Table([child])
        with pytest.raises(KeyError):
            table.get_parents(child)

    def test_get_spouse(self):
        husband = Person(1, "Husband", spouse_id=2)
        wife = Person(2, "Wife", spouse_id=1)
        table = Table([husband, wife])
        assert table.get_spouse(husband) == wife
        assert table.get_spouse(wife) == husband

    def test_get_spouse_no_result(self):
        person = Person(1, "Name")
        table = Table([person])
        assert table.get_spouse(person) == None

    def test_get_spouse_key_error(self):
        person = Person(1, "Name", spouse_id=999)
        table = Table([person])
        with pytest.raises(KeyError):
            table.get_spouse(person)

    def test_find_children(self):
        father = Person(1, "Father")
        mother = Person(2, "Mother")
        child1 = Person(3, "Child1", father_id=1, mother_id=2)
        child2 = Person(4, "Child2", father_id=1, mother_id=2)
        table = Table([father, mother, child1, child2])
        children = table.find_children(father, mother)
        assert len(children) == 2
        assert set(children) == {child1, child2}

    def test_find_children_no_result(self):
        person1 = Person(1, "Person1")
        person2 = Person(2, "Person2")
        table = Table([person1, person2])
        children = table.find_children(person1, person2)
        assert len(children) == 0


"""
Unittest for familytree.person module.
"""


from familytree.person import Person


class TestPerson:

    def test_init_minimal(self):
        p = Person(1, "Name")
        assert p.id_ == 1
        assert p.name == "Name"
        assert p.gender == None
        assert p.father_id == None
        assert p.mother_id == None
        assert p.birth_order == None
        assert p.spouse_id == None

    def test_init_full(self):
        p = Person(1, "Name", "F",
                   father_id=2, mother_id=3, birth_order=1,
                   spouse_id=4)
        assert p.id_ == 1
        assert p.name == "Name"
        assert p.gender == "F"
        assert p.father_id == 2
        assert p.mother_id == 3
        assert p.birth_order == 1
        assert p.spouse_id == 4


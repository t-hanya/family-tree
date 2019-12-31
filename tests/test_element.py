"""
Unittest for familytree.element module.
"""


from familytree.person import Person
from familytree.element import PersonBox
from familytree.element import SpouseLink
from familytree.element import ParentChildLink
from familytree.element import Figure


class TestPersonBox:

    def test_class_attr(self):
        assert type(PersonBox.width) == int
        assert type(PersonBox.height) == int
        assert PersonBox.width > 0
        assert PersonBox.height > 0

    def test_obj(self):
        person = Person(1, "Name")
        box = PersonBox(person, x=10, y=20)
        assert box.person == person
        assert box.xmin == 10
        assert box.ymin == 20
        assert box.xmax == (10 + box.width)
        assert box.ymax == (20 + box.height)

    def test_svg(self):
        person = Person(1, "Name")
        box = PersonBox(person, x=10, y=20)
        assert type(box.svg()) == str


class TestSpouseLink:

    def test(self):
        link = SpouseLink(10, 20, 30, 40)
        assert type(link.svg()) == str


class TestParentChildLink:

    def test(self):
        link = ParentChildLink(10, 20, 30, 40)
        assert type(link.svg()) == str


class TestFigure:

    def test(self):

        class DummyElement:
            xmin=10
            ymin=10
            xmax=20
            ymax=20
            person='person'

            def svg(self):
                return "SOME SVG STRING"

        figure = Figure([DummyElement()])
        svg = figure.svg()
        assert type(svg) == str
        assert "SOME SVG STRING" in svg

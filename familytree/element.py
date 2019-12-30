"""
Base objects in output diagram.
"""


from familytree.person import Person


PERSON_BOX_TEMPLATE = """
    <rect
     stroke="black" stroke-width="3" fill="white"
     x="{x}" y="{y}" width="{width}" height="{height}"></rect>
    <text
     x="{text_x}" y="{text_y}" writing-mode="tb"
     fill="black" glyph-orientation-vertical="0">
        {name}
    </text>
""".lstrip('\n')


SPOUSE_LINK_TEMPLATE = """
    <line
     x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"
     stroke="black" stroke-width="9" />
    <line
     x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"
     stroke="white" stroke-width="3" />
""".lstrip('\n')


PARENT_CHILD_LINK_TEMPLATE = """
    <polyline
     points="{x1},{y1} {x1},{ym} {x2},{ym} {x2},{y2}"
     stroke="black" stroke-width="4" fill="none" />
""".lstrip('\n')


class PersonBox:
    """Person information box element."""

    width: int = 60
    height: int = 180

    def __init__(self, person: Person, x: int, y: int) -> None:
        self.person = person
        self.x = x
        self.y = y

    @property
    def xmin(self) -> int:
        return self.x

    @property
    def ymin(self) -> int:
        return self.y

    @property
    def xmax(self) -> int:
        return self.x + self.width

    @property
    def ymax(self) -> int:
        return self.y + self.height

    def svg(self) -> str:
        """Return SVG element representation."""
        data = {
            'x': self.x,
            'y': self.y,
            'width': self.width,
            'height': self.height,
            'text_x': self.x + 30,
            'text_y': self.y + 20,
            'name': self.person.name
        }
        return PERSON_BOX_TEMPLATE.format(**data)


class SpouseLink:
    """Spouse link element."""

    def __init__(self, x1: int, y1: int, x2: int, y2: int) -> None:
        self._fields = {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2}

    def svg(self) -> str:
        """Return SVG element representation."""
        return SPOUSE_LINK_TEMPLATE.format(**self._fields)


class ParentChildLink:
    """Parent and child link element."""

    def __init__(self, x1: int, y1: int, x2: int, y2: int) -> None:
        self._fields = {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2}
        self._fields['ym'] = (y1 + 3 * y2) // 4

    def svg(self) -> str:
        """Return SVG element representation."""
        return PARENT_CHILD_LINK_TEMPLATE.format(**self._fields)


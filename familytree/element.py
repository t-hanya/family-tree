"""
Base objects in output diagram.
"""


import math

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

FIGURE_TEMPLATE = """
<?xml version="1.0" encoding="UTF-8"?>
<svg
 width="{width}px" height="{height}px"
 viewBox="{view_x} {view_y} {view_width} {view_height}"
 version="1.1" xmlns="http://www.w3.org/2000/svg">
  <g font-family="sans-serif" font-size="20">

{elements}
  </g>
</svg>
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


class Figure:
    """SVG figure."""

    def __init__(self, elements, width=640, height=480) -> None:
        self.width = width
        self.height = height
        self._elements = elements

    def svg(self) -> str:
        """Return SVG."""
        elements = '\n'.join([e.svg() for e in self._elements])

        # adjust view box coordinates so that
        # all elements are contained in this figure boundary.
        boxes = [e for e in self._elements if hasattr(e, 'person')]
        xmin = min([e.xmin for e in boxes])
        ymin = min([e.ymin for e in boxes])
        xmax = max([e.xmax for e in boxes])
        ymax = max([e.ymax for e in boxes])
        w = xmax - xmin
        h = ymax - ymin
        if w / h > self.width / self.height:
            if w > self.width:
                view_w = w
                view_h = int(math.ceil(self.height * w / self.width))
            else:
                view_w = self.width
                view_h = self.height
        else:
            if h > self.height:
                view_h = h
                view_w = int(math.ceil(self.width * h / self.height))
            else:
                view_w = self.width
                view_h = self.height

        margin_x = (view_w - w) // 2
        margin_y = (view_h - h) // 2
        view_x = xmin - margin_x
        view_y = ymin - margin_y

        return FIGURE_TEMPLATE.format(width=self.width,
                                      height=self.height,
                                      view_x=view_x,
                                      view_y=view_y,
                                      view_width=view_w,
                                      view_height=view_h,
                                      elements=elements)

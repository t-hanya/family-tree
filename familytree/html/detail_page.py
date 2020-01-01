"""
HTML
"""


from familytree.person import Person
from familytree.table import Table
from familytree.element import PersonBox
from familytree.element import Figure
from familytree.layout.butterfly import ButterflyLayout


HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
  <title>{page_title}</title>
  <meta charset="utf-8">
</head>
<body>
  <header>
    <a href="../index.html"><h1>Family Tree</h1></a>
  </header>
  <h2>{name}</h2>
  <h3>Family Tree</h3>
  {svg}
</body>
</html>
""".lstrip('\n')


PERSON_BOX_TEMPLATE = """
    <a href="{link}">
      <rect
       stroke="black" stroke-width="3" fill="white"
       x="{x}" y="{y}" width="{width}" height="{height}"></rect>
      <text
       x="{text_x}" y="{text_y}" writing-mode="tb"
       fill="black" glyph-orientation-vertical="0">
          {name}
      </text>
    </a>
""".lstrip('\n')


class LinkedPersonBox(PersonBox):
    """Extended person box element with hyperlink."""

    def svg(self) -> str:
        """Return SVG element representation."""
        data = {
            'x': self.x,
            'y': self.y,
            'width': self.width,
            'height': self.height,
            'text_x': self.x + 30,
            'text_y': self.y + 20,
            'name': self.person.name,
            'link': './{}.html'.format(self.person.id_)
        }
        return PERSON_BOX_TEMPLATE.format(**data)


def render_detail_page(table: Table, person: Person) -> str:
    """Render detail page HTML content."""

    layout_func = ButterflyLayout(
        person_box_class=LinkedPersonBox)
    figure = Figure(layout_func(table, person))
    html = HTML_TEMPLATE.format(
        page_title='Family Tree - {}'.format(person.name),
        name=person.name,
        svg=figure.svg())
    return html

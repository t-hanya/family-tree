"""
HTML
"""


from familytree.person import Person
from familytree.table import Table


HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
  <title>Family Tree</title>
  <meta charset="utf-8">
</head>
<body>
  <header>
    <a href="./index.html"><h1>Family Tree</h1></a>
  </header>
  <h2>Index</h2>
  <ul>
    {link_list}
  </ul>
</body>
</html>
""".lstrip('\n')


LIST_ITEM_TEMPLATE = """
    <li>
      <a href="./details/{person_id}.html">{name}</a>
    </li>
"""


def render_index_page(table: Table) -> str:
    """Render index page HTML content."""

    link_list = ''
    for person in table:
        link_list += LIST_ITEM_TEMPLATE.format(
            person_id=person.id_,
            name=person.name)

    html = HTML_TEMPLATE.format(
        link_list=link_list)
    return html
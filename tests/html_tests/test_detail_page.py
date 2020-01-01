"""
Unittest for detail page module.
"""


from familytree.person import Person
from familytree.table import Table
from familytree.html.detail_page import render_detail_page


class TestRenderDetailPage:

    def test(self):
        table = Table([Person(1, "Name", "M", spouse_id=2),
                       Person(2, "Name", "F", spouse_id=1)])
        html = render_detail_page(table, table.get(1))
        assert 'svg' in html
        assert '2.html' in html

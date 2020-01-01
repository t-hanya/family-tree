"""
Unittest for index page module.
"""


from familytree.person import Person
from familytree.table import Table
from familytree.html.index_page import render_index_page


class TestRenderDetailPage:

    def test(self):
        table = Table([Person(1, "Name", "M", spouse_id=2),
                       Person(2, "Name", "F", spouse_id=1)])
        html = render_index_page(table)
        print(html)
        assert False
        assert './details/1.html' in html
        assert './details/2.html' in html

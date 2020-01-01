"""
Unittest for familytree.csv_parser module.
"""


from pathlib import Path
from tempfile import TemporaryDirectory

from familytree.csv_parser import parse_csv
from familytree.person import Person
from familytree.table import Table


SAMPLE_CSV = """
id,family_name,first_name,gender,father_id,mother_id,birth_order,spouse_id
 1,        XXX,       AAA,     M,         ,         ,           ,        2
 2,        XXX,       BBB,     F,         ,         ,           ,        1
 3,        XXX,       CCC,     M,        1,        2,          1,
""".lstrip('\n')


class TestParseCsv:

    def test(self):
        with TemporaryDirectory() as tmp_dir:
            tmp_dir = Path(tmp_dir)
            csv_path = tmp_dir / 'sample.csv'
            with csv_path.open('w') as f:
                f.write(SAMPLE_CSV)

            table = parse_csv(str(csv_path))

        assert len(table) == 3

        persons = list(table)
        assert persons[0] == Person(1, "XXX AAA", "M", spouse_id=2)
        assert persons[1] == Person(2, "XXX BBB", "F", spouse_id=1)
        assert persons[2] == Person(3, "XXX CCC", "M",
                                    father_id=1, mother_id=2, birth_order=1)

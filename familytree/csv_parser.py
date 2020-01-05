"""
CSV file parser.
"""


from typing import Union

from familytree.person import Person
from familytree.table import Table


INT_VAL_HEADERS = ['id_', 'father_id', 'mother_id', 'birth_order', 'spouse_id']


def _convert_key(key: str) -> str:
    if key == 'id':
        return 'id_'
    else:
        return key

def _convert_value(key: str, value: str) -> Union[str, int]:
    if value == '':
        return None
    elif key in INT_VAL_HEADERS:
        return int(value)
    else:
        return value


def parse_csv(csv_file: str) -> Table:
    """Parse family tree data CSV."""
    with open(csv_file) as f:
        lines = f.readlines()
    lines = [l.strip() for l in lines if l.strip()]

    # parse header row
    headers = [s.strip() for s in lines[0].split(',')]
    headers = [_convert_key(s) for s in headers]

    # parse content row
    persons = []
    for line in lines[1:]:
        if len(line.strip()) == 0:
            continue
        values = [s.strip() for s in line.split(',')]
        assert len(headers) == len(values)

        data = {k: _convert_value(k, v)
                for k, v in zip(headers, values)}

        if 'family_name' in data and 'first_name' in data:
            data['name'] = '{} {}'.format(data['family_name'],
                                          data['first_name'])
            del data['family_name']
            del data['first_name']

        persons.append(Person(**data))

    return Table(persons)

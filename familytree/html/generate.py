"""
Generate family tree HTML document.
"""


import argparse
from pathlib import Path

from familytree.csv_parser import parse_csv
from familytree.html.index_page import render_index_page
from familytree.html.detail_page import render_detail_page


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('csv_file', type=str,
                        help='Famly data CSV file path')
    parser.add_argument('--output', type=str, default='output',
                        help='Output directory path')
    args = parser.parse_args()
    return args


def main():
    """Main function."""
    args = parse_args()
    table = parse_csv(args.csv_file)

    output_dir = Path(args.output)
    detail_dir = output_dir / 'details'
    detail_dir.mkdir(parents=True, exist_ok=True)

    index_html = render_index_page(table)
    with (output_dir / 'index.html').open('w') as f:
        f.write(index_html)

    for person in table:
        detail_html = render_detail_page(table, person)
        detail_html_path = detail_dir / '{}.html'.format(person.id_)
        with detail_html_path.open('w') as f:
            f.write(detail_html)


if __name__ == '__main__':
    main()

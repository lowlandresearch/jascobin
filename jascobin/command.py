import csv
import io
from pathlib import Path

import click

from . import jws

def print_csv(data):
    columns = ['x'] + [f'y{i + 1}' for i in range(data.header.channels)]
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(columns)
    writer.writerows(zip(data.x, *data.y))
    print(buf.getvalue())

def get_data(path: Path):
    loaders = {
        '.jws': jws.load_jws,
    }
    return loaders.get(path.suffix, lambda p: None)(path)

@click.group()
def main():
    pass

@click.command()
@click.argument('path', type=click.Path(exists=True))
def to_csv(path):
    path = Path(path)

    data = get_data(path)
    
    if data:
        print_csv(data)

main.add_command(to_csv)

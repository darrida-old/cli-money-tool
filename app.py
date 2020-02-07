# Standard Library
import sqlite3
from pathlib import *

# PYPI
import click

# Local
import db_classes as data
import import_classes as imp

home_dir = Path.home()

@click.group()
def cli():
    '''Hammond Finance cli'''

@cli.command('import', help='Import from financial institutions')
@click.argument('b', 'bank')
def file_imports(bank):
    bank = bank.lower()
    if bank == 'oldsecond':
        imp.import_oldsecond('download.CSV')

#with data.database() as db:
#    db.create_tables()
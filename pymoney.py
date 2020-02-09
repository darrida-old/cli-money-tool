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
    '''Money cli'''

@cli.command('import', help='Import data from financial institutions.' \
'                            ARGUMENTS: oldsecond, capitalone, chase, paypal, edwardjones' \
'                            Note: input name of institutione exactly how it\'s displayed.')
@click.argument('bank')
def file_imports(bank):
    bank = bank.lower()
    if bank == 'oldsecond':
        imp.import_oldsecond('download (1).CSV') #'checking_transactions.csv')
    elif bank == 'capitalone':
        imp.import_capitalone('capitalone_transactions.csv')
    elif bank == 'chase':
        imp.import_chase('chase_transactions.csv')
    elif bank == 'paypal':
        imp.import_paypal('paypal_transactions.csv')
    elif bank == 'edwardjones':
        imp.import_edwardjones('edwardjobs_transactions.csv')
    else:
        click.echo('Input name is not known.')
# Standard Library
from pathlib import Path

# PYPI
import click

# Local
import db_classes as data
import import_classes as imp

home_dir = Path.home()
data_location = str(Path("<path here>"))


@click.group()
def cli():
    """Money cli."""


@cli.command("setup", help="Configure location(s) of file and sqlite database.")
def pymoney_setup():
    pass


@cli.command(
    "import",
    help="Import data from financial institutions.                             "
    "-----------------------------------------------------------                             "
    "ARGUMENTS: oldsecond, capitalone, chase, paypal, edwardjones",
)
@click.argument("bank")
def file_imports(bank):
    bank = bank.lower()
    if bank == "oldsecond":
        imp.import_oldsecond("checking_transactions.csv")
    elif bank == "capitalone":
        imp.import_capitalone("capitalone_transactions.csv")
    elif bank == "chase":
        imp.import_chase("chase_transactions.csv", data_location)
    elif bank == "paypal":
        imp.import_paypal("paypal_transactions.csv")
    elif bank == "edwardjones":
        imp.import_edwardjones("edwardjobs_transactions.csv")
    else:
        click.echo("Input name is not known.")


@cli.command(
    "sum",
    help="Sums all transactions from financial institutions                             "
    "-----------------------------------------------------------                             "
    "ARGUMENTS: oldsecond, capitalone, chase, paypal, edwardjones",
)
@click.argument("bank")
def transactions_sum(bank):
    bank = bank.lower()
    if bank == "chase":
        account = "credit_chase"
    if bank == "oldsecond":
        account = "Checking"
    if bank == "capitalone":
        pass
    if bank == "paypal":
        pass
    if bank == "edwardjones":
        pass
    # if bank == 'all':
    #    account = '*'
    with data.database() as db:
        result = db.sum_transactions_all(account)
        print(result)

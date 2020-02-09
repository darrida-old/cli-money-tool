# Standard
import csv
import pprint

# PYPI
import click

# Local
import db_classes as data

def import_oldsecond(name):
    # IMPORT OLDSECOND CSV FILE
    data_location = '..\_appdata\cli_money_tool\\'
    reader = csv.DictReader(open(data_location + name, 'r'))
    dict_list = []
    for line in reader:
        dict_list.append(line)
    total = 0

    with data.database() as db:
        # QUERY EXISTING RECORDS IN TRANSACTIONS TABLE
        count = 0
        existing = db.execute('''SELECT * FROM transactions''').fetchall()
        click.echo(f'Existing Transactions: {str(len(existing))}')
        for i in dict_list:
            insert = True
            if len(existing) > 0:
                # CHECK IF MATCHING RECORD EXISTS ALREADY. IF SO, INSERT = FALSE
                for transaction in existing:
                    if (transaction[1].replace(" ", "") == i['Account Designator'].replace(" ", "") and \
                        transaction[2].replace(" ", "") == i['Posted Date'].replace(" ", "") and \
                        transaction[3].replace(" ", "") == i['Description'].replace(" ", "") and \
                        float(transaction[4]) == ((float(i['Amount']) * -1) if i['CR/DR'] == 'DR' else float(i['Amount'])) and \
                        float(transaction[5]) == float(i['Serial Number'])) == True:
                        insert = False
            if insert:
                if i['CR/DR'] == 'DR':
                    i['Amount'] = str(float(i['Amount']) * -1)
                record = data.transactions(
                    id=None,
                    account=i['Account Designator'].strip(),
                    date=i['Posted Date'],
                    description=i['Description'],
                    amount=i['Amount'],
                    misc=i['Serial Number']
                )
                db.insert(record)
                count += 1
    click.echo(f'Added Transactions: {count}')

def import_chase(name):
    pass

def import_paypal(name):
    pass

def import_edwardjones(name):
    pass
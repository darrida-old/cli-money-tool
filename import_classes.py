# Standard
import csv
from pathlib import Path
import sqlite3

# PYPI
import click

# Local
import db_classes as data


def import_oldsecond(name: str):
    """DESCRIPTION: Import Old Second CSV File

    Arguments:
        name (string): file name
    """

    try:
        data_location = "..\\_appdata\\cli_money_tool\\"
        reader = csv.DictReader(open(data_location + name, "r"))
        dict_list = []
        for line in reader:
            dict_list.append(line)

        with data.database() as db:
            # QUERY EXISTING RECORDS IN TRANSACTIONS TABLE
            count = 0
            existing = db.execute(
                """SELECT * FROM transactions WHERE account = 'Checking' """
            ).fetchall()
            click.echo(f"Existing Transactions: {str(len(existing))}")
            for i in dict_list:
                insert = True
                if len(existing) > 0:
                    # CHECK IF MATCHING RECORD EXISTS ALREADY. IF SO, INSERT = FALSE
                    for transaction in existing:
                        if (
                            transaction[1].replace(" ", "") == i["Account Designator"].replace(" ", "")
                            and transaction[2].replace(" ", "") == i["Posted Date"].replace(" ", "")
                            and transaction[3].replace(" ", "") == i["Description"].replace(" ", "")
                            and float(transaction[4]) == (
                                                        (float(i["Amount"]) * -1)
                                                        if i["CR/DR"] == "DR"
                                                        else float(i["Amount"])
                                                    )
                            and float(transaction[5]) == float(i["Serial Number"])
                        ) is True:
                            insert = False
                if insert:
                    if i["CR/DR"] == "DR":
                        i["Amount"] = str(float(i["Amount"]) * -1)
                    record = data.transactions(
                        id=None,
                        account=i["Account Designator"].strip(),
                        date=i["Posted Date"],
                        description=i["Description"],
                        amount=i["Amount"],
                        misc=i["Serial Number"],
                    )
                    db.insert(record)
                    count += 1
        click.echo(f"Added Transactions: {count}")
    except FileNotFoundError as e:
        click.echo(
            "UPLOAD FAILED: File needed for upload not found. Check existence of file or file name."
        )
        click.echo(f"ERROR MESSAGE: {e}")
    except sqlite3.OperationalError as e:
        click.echo(
            "UPLOAD FAILED: Table in database was not found. Check existence of database or table. May need to run install.bat again."
        )
        click.echo(f"ERROR MESSAGE: {e}")


def import_chase(name: str, data_location: str):
    """DESCRIPTION: Import Chase CSV file

    Arugments:
        name (string): file name
        
        data_location (string): file location
    """

    try:
        reader = csv.DictReader(open(data_location + "\\" + name, "r"))
        dict_list = []
        for line in reader:
            dict_list.append(line)
        with data.database() as db:
            # QUERY EXISTING RECORDS IN TRANSACTIONS TABLE
            count = 0
            existing = db.execute(
                """SELECT * FROM transactions WHERE account = 'credit_chase' """
            ).fetchall()
            click.echo(f"Existing Transactions: {str(len(existing))}")
            for i in dict_list:
                insert = True
                if len(existing) > 0:
                    # CHECK IF MATCHING RECORD EXISTS ALREADY. IF SO, INSERT = FALSE
                    for transaction in existing:
                        if (
                            transaction[1].replace(" ", "") == "credit_chase"
                            and transaction[2].replace(" ", "") == i["Post Date"].replace(" ", "")
                            and transaction[3].replace(" ", "") == i["Description"].replace(" ", "")
                            and float(transaction[4]) == float(i["Amount"])
                            and transaction[5] == "None"
                        ) is True:  # float(i['Serial Number'])) == True:
                            insert = False
                if insert:
                    record = data.transactions(
                        id=None,
                        account="credit_chase",
                        date=i["Post Date"],
                        description=i["Description"],
                        amount=i["Amount"],
                        misc=None,
                    )
                    db.insert(record)
                    count += 1
        click.echo(f"Added Transactions: {count}")
    except FileNotFoundError as e:
        click.echo(
            "UPLOAD FAILED: File needed for upload not found. Check existence of file or file name."
        )
        click.echo(f"ERROR MESSAGE: {e}")
    except sqlite3.OperationalError as e:
        click.echo(
            "UPLOAD FAILED: Table in database was not found. Check existence of database or table."
        )
        click.echo(f"ERROR MESSAGE: {e}")


def import_paypal(name: str):
    pass


def import_edwardjones(name: str):
    pass


def import_capitalone(name: str):
    pass

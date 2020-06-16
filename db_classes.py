# Standard
import sqlite3
import os
from pathlib import Path


class transactions:
    """Intended use is with an insert function into the transation table.
    
    This class is passed into the db_banner.database function.
    """
    def __init__(self, id, account, date, description, amount, misc):
        self.id = id
        self.account = account
        self.date = date
        self.description = description
        self.amount = amount
        self.misc = misc


class tags:
    """Not currently in use. Intended use is with an insert function into the tags table.
    """
    def __init__(self, id, tag):
        self.id = id
        self.tag = tag


class tags_link:
    """Not currently in use. Intended use is with an insert function into the tags_link table.
    """
    def __init__(self, id, id_tag, id_transaction):
        self.id = id
        self.id_tag = id_tag
        self.id_transaction = id_transaction


class database(object):
    """Handles all database connectsion, inputs, and outputs

    Class constructor initiates sqlite3 database connection. If used in WITH statement
    the connection will cleanly close after the statement is finished. If there are
    uncommitted transactions they will be rolled back prior to connection closure.
    """
    def __init__(self):
        __DB_LOCATION = (
            Path.home()
            / "Documents"
            / "GitHub"
            / "_appdata"
            / "cli_money_tool"
            / "accounts.db"
        )
        if not os.path.exists(__DB_LOCATION):
            Path(
                Path.home() / "Documents" / "GitHub" / "_appdata" / "cli_money_tool"
            ).mkdir(parents=True, exist_ok=True)
        self.__db_connection = sqlite3.connect(str(__DB_LOCATION))
        self.cur = self.__db_connection.cursor()

    def __del__(self):
        self.__db_connection.close()

    def __enter__(self):
        return self

    def __exit__(self, ext_type, exc_value, traceback):
        self.cur.close()
        if isinstance(exc_value, Exception):
            self.__db_connection.rollback()
        else:
            self.__db_connection.commit()
        self.__db_connection.close()

    def execute(self, new_data: str) -> tuple:
        """Executes an valid SQL statement passed through as a string.

        Arugments:
            new_data (string): Valid SQL statement
        """
        return self.cur.execute(new_data)

    def executemany(self, many_new_data: str) -> None:
        """Not currently in use.
        """
        self.cur.executemany("REPLACE INTO jobs VALUES(?, ?, ?, ?)", many_new_data)

    def insert(self, record):
        """Inserts a transaction record. Designed for use with the transaction class.

        Arguments:
            record (transaction class): class or dictionary containing the following values:

                - id
                - account
                - date
                - description
                - amount
                - misc
        """
        record.id = self.cur.execute("""SELECT MAX(id) FROM transactions""").fetchone()[0]
        record.id = record.id + 1 if record.id else 1
        self.cur.execute(
            f"""INSERT INTO transactions
                             VALUES (
                                        "{record.id}",
                                        "{record.account}",
                                        "{record.date}",
                                        "{record.description}",
                                        "{record.amount}",
                                        "{record.misc}"
                        )"""
        )

    def create_tables(self):
        """This function confirms the existence of or creates the path, database, and tables.

        Can be used by calling the function directly, but is designed to by used by install.py, which is called by the install.bat file.
        """
        if not (
            Path.home()
            / "Documents"
            / "GitHub"
            / "_appdata"
            / "cli_money_tool"
            / "accounts.db"
        ):
            Path(Path.cwd() / ".." / "_appdata" / "cli_money_tool").mkdir(
                parents=True, exist_ok=True
            )

        """create a database table if it does not exist already"""
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS
                                "transactions" (
                                    "id"            INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                    "account"    	TEXT NOT NULL,
                                    "date"	        TEXT NOT NULL,
                                    "description"	TEXT,
                                    "amount"	    INTEGER NOT NULL,
                                    "misc"          INTEGER
                        )"""
        )
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS
                                "tags_link" (
                                    "id"	          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                    "id_tag"	      INTEGER NOT NULL,
                                    "id_transaction"  INTEGER NOT NULL
                        )"""
        )
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS
                                "tags" (
                                    "id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                    "tag"	TEXT NOT NULL
                        )"""
        )

    def select_all_transactions(self) -> tuple:
        """Returns all transactions

        Returns:
            tuple: contains all existing transactions in transaction table.
        """
        return self.cur.execute("""SELECT * FROM transactions""").fetchall()

    def sum_transactions_all(self, account: str) -> int:
        """Sums all transactions for specified account.

        Arguments:
            account (string): selected account/institution

        Returns:
            tuple: contains single value of rounded (2 decimal paces) result.
        """
        all_amounts = self.cur.execute(
            f"""SELECT amount FROM transactions
                                           WHERE account = '{account}'
                                        """
        ).fetchall()
        calc = 0
        for i in all_amounts:
            calc += float(i[0])
        return round(calc, 2)

    def commit(self):
        """Use after any other database class function to commit changes.

        This function is separated from initial transactions to enable the __exit__ function to rollback changes in the case that errors are encountered.
        """
        self.__db_connection.commit()

# Standard
import sqlite3
from pathlib import *

# Local
import db_classes as data

with data.database() as db:
    db.create_tables()
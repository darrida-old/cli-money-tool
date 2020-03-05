# CLI-MONEY-TOOL

Note: This is very much in progress. Not setup wizard exists yet, so it may be difficult to enable it to function in your environment.

This CLI allows the import and exploration of data from CSV files exported from financial institutions

## Setup

### Windows

- Clone repository
- Launch install.bat

### Linux (not tested much, but should work)

- Clone reponsitory
- Open the Terminal to the same directory as the repository and run the following:

```cmd
python -m pip install --editable .
python install.py
```

### Setup Summary

The install process will do the following:

- Sets up ```pymoney``` as a global CMD command (the install.bat file does not use a virtual environment)
- Creates the pymoney database and the needed tables

Note: this tool is lightweight in terms of libraries, since the only non-standard library that it uses is Click.

## Usage

### Explore CLI Options

```cmd
C:\Users\User>pymoney

Usage: pymoney [OPTIONS] COMMAND [ARGS]...

  Money cli.

Options:
  --help  Show this message and exit.

Commands:
  import  Import data from financial institutions.
  setup   Configure location(s) of file and sqlite database.
  sum     Sums all transactions from financial institutions...
```

- The commands reveal more information as well

```cmd
C:\Users\User>pymoney import --help
Usage: pymoney import [OPTIONS] BANK

  Import data from financial institutions.
  -----------------------------------------------------------
  ARGUMENTS: oldsecond, capitalone, chase, paypal, edwardjones


C:\Users\User>pymoney setup --help
Usage: pymoney setup [OPTIONS]

  Configure location(s) of file and sqlite database.


C:\Users\User>pymoney sum --help
Usage: pymoney sum [OPTIONS] BANK

  Sums all transactions from financial institutions
  -----------------------------------------------------------
  ARGUMENTS: oldsecond, capitalone, chase, paypal, edwardjones
  ```
  
### Explore CLI Commads

#### ```import```

- Results:
  - Total number of transactions for the requested institution that are currently in the database.
  - Total number of new transactions added to the database.

```cmd
C:\Users\Users\GitHub\cli-money-tool>pymoney import superbank
Existing Transactions: 225
Added Transactions: 0
```

#### ```sum```

- Totals all transactions for a requested institution.

```cmd
C:\Users\User\GitHub\cli-money-tool>pymoney sum superbank
-367.6
```

#### ```setup```

- [Placeholder]

# Standard
import csv
import pprint

# Local
import db_classes as data

def import_oldsecond(name):
    data_location = '..\_appdata\cli_money_tool\\'
    reader = csv.DictReader(open(data_location + name, 'r'))
    
    dict_list = []
    for line in reader:
        dict_list.append(line)
    total = 0

    with data.database() as db:
        for i in dict_list:
            print(i)
            if i['CR/DR'] == 'DR':
                i['Amount'] = str(float(i['Amount']) * -1)
            record = data.transactions(
                id=None,
                account=i['Account Designator'],
                date=i['Posted Date'],
                description=i['Description'],
                amount=i['Amount'],
                misc=i['Serial Number']
            )
            print(record)
            db.insert(record)
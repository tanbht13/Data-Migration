import pandas as pd

import database


db_type = input("Please enter client's db: mssql, postgres, oracle\n")
db_type = db_type.lower()
if db_type == 'oracle':
    engine_client = database.ask_oracle()

if db_type == 'mssql':
    engine_client = database.ask_mssql()

if db_type == 'postgres':
    engine_client = database.ask_postgres()

db_type_our = input("Please enter your db: mssql, postgres, oracle\n")
db_type_our = db_type_our.lower()
if db_type_our == 'postgres':
    engine_our = database.ask_postgres()

    if db_type_our == 'mssql':
        engine_our = database.ask_mssql()

    if db_type_our == 'postgres':
        engine_our = database.ask_postgres()

    table_name = input('\nInput the table name to fetch:\n')
    query = 'select * from {}'.format(table_name)
    df_client = pd.read_sql(query, database.ask_postgres())
    our_table = input('\nInput the table name you want in your db\n')
    df_client.to_sql(our_table, engine_our, if_exists='replace')
    print('\nTable Updated.')


import cx_Oracle
from sqlalchemy import create_engine


# # Connection to oracle db
def connect_oracle(credentials):
    dsn = cx_Oracle.makedsn(credentials['host'], credentials['port'], sid=credentials['sid'])
    connection = cx_Oracle.connect(credentials['username'], credentials['password'], dsn)
    return connection


def ask_oracle():
    host = input('\nPlease enter the hostname:like localhost \n')
    user = input('\nPlease enter the username: like test_user \n')
    sid = input('\nPlease enter the sid name: \n')
    port = input('\nPlease enter the port no: \n')
    password = input('\nPlease enter the password: \n')

    oracle_connection = {'host': host, 'port': port, 'sid': sid,
                         'username': user,
                         'password': password}
    connection = connect_oracle(oracle_connection)
    return connection


def ask_mssql():
    db_name = input('\nPlease enter the db name: doctor\n')
    user = input('\nPlease enter the username: LAPTOP-G6ROMIL9\Admin\n')
    password = input('\nPlease enter the password: password\n')
    engine = create_engine(
        "mssql+pymssql://{}:{}@localhost/{}".format(user, password,
                                                    db_name))
    return engine


def ask_postgres():
    host = input('\nPlease enter the host number: 127.0.0.1\n')
    db_name = input('\nPlease enter the db name: tanyadb\n')
    user = input('\nPlease enter the username: postgres\n')
    password = input('\nPlease enter the password: tanya13\n')
    db_string = "postgres+psycopg2://{}:{}@{}/{}".format(user, password,
                                                         host,
                                                         db_name)
    engine = create_engine(db_string)
    return engine

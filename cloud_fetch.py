from __future__ import print_function
import httplib2
import oauth2client
import os
import googleapiclient
import openpyxl
from sqlalchemy import create_engine
import pandas as pd
import cx_Oracle
import json
import datetime
from googleapiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from openpyxl import Workbook
from pandas import DataFrame, ExcelWriter
import google.protobuf


""" This is the code to get raw data from a specific Google Sheet"""
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret_noemail.json'
APPLICATION_NAME = 'Migration App'

def ask_mssql():
    engine = create_engine('mssql+pyodbc://@' + 'LAPTOP-G6R0MIL9\SQLEXPRESS' + '/' + 'doctor' + '?driver=SQL+Server')
    return engine


def get_credentials():
    """Gets valid user credentials from storage.
    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.
    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run_flow(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def main():
    """Shows basic usage of the Sheets API.
    Creates a Sheets API service object and prints the names and majors of
    students in a sample spreadsheet:
    https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?version=v4')
    service = googleapiclient.discovery.build(
        'sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)

    # Google Sheet Url Link and Range name. Can use tab names to get full page.
    spreadsheetId = '19N5CglbGW6RynG-_-w37zKdkvIbtRsBR3MMyIlr1xD8'
    rangeName = 'Sheet1'

    response = service.spreadsheets().values().get(spreadsheetId=spreadsheetId,majorDimension='ROWS',
                                                    range=rangeName).execute()
    columns= response['values'][0]
    data=response['values'][1:]
    df=pd.DataFrame(data, columns=columns)
    print(df)
    engine_client = ask_mssql()
    our_table = ask_mssql()
    query2 = 'select * from {}'.format('doctor_tbl')
    df_our = pd.read_sql(query2, engine_client)
    lc = df.values.tolist()
    lo = df_our.values.tolist()
    if len(lc) != len(lo):
        diff = lc[len(lo):len(lc)]
        lo.extend(diff)

    for i in range(len(lo)):
        for j in range(len(df_our.columns)):
            if lo[i][j] != lc[i][j]:
                lo[i][j] = lc[i][j]

    headers = [col for col in df_our.columns]

    df = pd.DataFrame(data=lo, columns=headers)
    df.to_sql('doctor_tbl', engine_client, if_exists='replace', index=False)

    print('\nTable Updated.')
if __name__ == '__main__':
    main()
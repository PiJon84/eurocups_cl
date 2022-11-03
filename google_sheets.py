from __future__ import print_function
import httplib2
import os
import time

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import load_bets

import argparse
flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'#.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'CLTournament'

SID_CL = '1cFZqWsC5POWXijlUvFezCkBPbkan6kWtZXjH1l_QeTE'
SID_EC = '1Nz9hlWQmrV6_2ZU0QI-gwZuGSHlrlyJb4qIJ_C5ipJg'
#SID_SS = '1K_5KjtS_CdAN7-bUjHndZQtoprZs57nylPVGdGg0UYg'

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
    credential_path = os.path.join(credential_dir, 'python-cltournament.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to ' + credential_path)
    return credentials

def open_sheet():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    return discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)

def get_last_data(service, sheet_id, list_name, col_name):
    range_name = list_name + '!' + col_name + ':' + col_name
    result = service.spreadsheets().values().get(spreadsheetId=sheet_id, range=range_name).execute()
    values = result.get('values', [])
    return (len(values)+1, int(values[-1][0])+1)

def update_data_in_sheet(service, sheet_id, range_name, values):
    val = {"values": values}
    result = service.spreadsheets().values().update(spreadsheetId=sheet_id, range=range_name, valueInputOption="RAW", body=val).execute()
    print('Done!')
    return True

def update_cl(stage):
    sheet_id = SID_CL
    list_name = 'Прогнозы'
    
    sh = open_sheet()
    start_row, first_game = get_last_data(sh, sheet_id, list_name, 'A')
    bets = load_bets.get_bets(stage)

    end_row = start_row - 1
    values = []
    
    for usr,bet in bets.items():
        i = first_game
        for b in bet:
            try:
                a1 = int(b[-3])
                a2 = int(b[-1])
            except Exception as e:
                a1 = 10
                a2 = 10
                print('Ошибка при чтении ставки ', usr)
              
            values.append([i, usr, a1, a2])
            end_row += 1
            i += 1

    if end_row >= start_row:
        range_name = list_name + '!A' + str(start_row) + ':D' + str(end_row)
        update_data_in_sheet(sh, sheet_id, range_name, values)

def update_ec(stage):
    sheet_id = SID_EC
    list_name = 'Прогнозы'
    
    sh = open_sheet()
    start_row, first_game = get_last_data(sh, sheet_id, list_name, 'B')
    bets = load_bets.get_bets(stage)

    end_row = start_row - 1
    values = []
    
    for usr,bet in bets.items():
        i = first_game
        for b in bet:
            ls = b.rfind(' ')
            if ls > -1:
                v = b[ls+1:].replace('х', 'X').replace('Х', 'X').replace('x', 'X')
            else:
                v = b

            values.append([i, usr, v])
            end_row += 1
            i += 1

    if end_row >= start_row:
        range_name = list_name + '!B' + str(start_row) + ':D' + str(end_row)
        update_data_in_sheet(sh, sheet_id, range_name, values)

def update_ss(stage, tour):
    sheet_id = SID_SS
    list_name = 'Прогнозы'
    
    sh = open_sheet()
    start_row, first_game = get_last_data(sh, sheet_id, list_name, 'C')
    bets = load_bets.get_bets(stage)

    end_row = start_row - 1
    values = []
    
    for usr,bet in bets.items():
        for b in bet:
            values.append([tour, usr, b])
            end_row += 1

    if end_row >= start_row:
        range_name = list_name + '!C' + str(start_row) + ':E' + str(end_row)
        update_data_in_sheet(sh, sheet_id, range_name, values)        
    
    
if __name__ == '__main__':

   # Лига чемпионов
   # update_cl(548)
   # update_cl(546)   

   # Чемпионат Еврокапса
    update_ec(564)


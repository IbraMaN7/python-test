from celery import shared_task

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import os.path
from datetime import date

import requests, xml.etree.ElementTree as ET

from .views import up_base


@shared_task()
def update_base():
    datasheets = data_from_sheets()
    price_ru = quotation_USD()
    up_base(datasheets, price_ru)

def quotation_USD():
    res = requests.get("https://www.cbr.ru/scripts/XML_daily.asp?date_req=" +
                       '{2}/{1}/{0}'.format(*str(date.today()).split('-'))) #02/03/2022
    res_xml = ET.fromstring(res.text)
    for main_tag in res_xml.iter('Valute'):
        if main_tag.attrib.get('ID') == 'R01235':
            return main_tag.find('Value').text

def data_from_sheets():
    SCOPES = ['https://www.googleapis.com/auth/drive']

    DOCUMENT_ID = '1z2GZ-R9MZwiEhBLo85hkWL6Om8bQKG1cNsm837H37bk'
    creds = None

    if os.path.exists('token.json'):
        creds =  Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    spreadsheet_id = '1z2GZ-R9MZwiEhBLo85hkWL6Om8bQKG1cNsm837H37bk'
    range_name = 'Sheet1'

    try:
        service = build('sheets', 'v4', credentials=creds)

        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range=range_name).execute() #, range=range_name
        rows = result.get('values', [])
        rows = rows[1:]
        return rows
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error
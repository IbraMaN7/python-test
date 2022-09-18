from celery import shared_task

from .views import up_base
from project.settings import SCOPES, SPREADSHEET_ID

import requests, xml.etree.ElementTree as ET

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import os.path
from datetime import date


@shared_task()
def update_base():
    """
    Update data in database
    1. Get creds
    2. Get data from sheet with creds (data)
    3. Get quotation USD (price_ru)
    4. Call function 'ud_date' from 'views' with 'data' and 'price_ru'
    """
    creds = get_creds(scopes=SCOPES)
    data = get_data_from_sheet(spreadsheet_id=SPREADSHEET_ID, 
                               range_name='Sheet1', 
                               creds=creds)
    price_ru = get_quotation_USD()
    up_base(data, price_ru)

def get_quotation_USD() -> float:
    """
    Get usd course with Bank of Russia
    """
    res = requests.get("https://www.cbr.ru/scripts/XML_daily.asp?date_req=" +
                       '{2}/{1}/{0}'.format(*str(date.today()).split('-')))
                       #02/03/2022
    res_xml = ET.fromstring(res.text)
    for main_tag in res_xml.iter('Valute'):
        if main_tag.attrib.get('ID') == 'R01235':
            return round(float(main_tag.find('Value').text.replace(',', '.')), 5)
             

def get_creds(scopes):
    """
    Get credentials Google API
    If there is no "token.json" file, 
    it is created from the "credentials.json" file
    :param scopes:
    :type list:
    """

    creds = None

    if os.path.exists('token.json'):
        creds =  Credentials.from_authorized_user_file('token.json', scopes)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', scopes)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds

def get_data_from_sheet(spreadsheet_id, range_name, creds) -> list:
    """
    Get data from sheet
    :param spreadsheets_id:
    :type string:
    :param range_name:
    :type string:
    :param creds:
    :type Credentials:
    """
    try:
        service = build('sheets', 'v4', credentials=creds)

        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range=range_name).execute()
        rows = result.get('values', [])
        return rows[1:]
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error
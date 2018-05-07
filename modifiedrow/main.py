import os
import boto3
import json
import urllib.request

gsheets_url = "https://sheets.googleapis.com/v4/spreadsheets/"

def handler(event, context):
  #remove credentials from event
  accesstoken = event['accesstoken']
  event['accesstoken'] = '***'

  print("event")
  print(event)

  sheetid = event['sheetid']
  request = urllib.request.Request(gsheets_url+sheetid+'?includeGridData=true')
  request.add_header('Authorization','Bearer '+accesstoken)
  result = []
  with urllib.request.urlopen(request) as response:
    content = response.read()
    # {"spreadsheetId": "14QSVK1EA8NbSyo9F3P25GaWAwDCXpHd9i473XoQZZlc",
    #  "properties": {
    #    "title": "Aufragsbuch",
    #    "locale": "de_DE",
    #    "autoRecalc": "ON_CHANGE",
    #    "timeZone": "Europe/Berlin",
    #    "defaultFormat": {...}
    #   }
    #  },
    #  "sheets": [
    # {
    #   "properties": {
    #     "sheetId": 0,
    #     "title": "Tabellenblatt1",
    #     "index": 0,
    #     "sheetType": "GRID",
    #     "gridProperties": {
    #         "rowCount": 1000,
    #         "columnCount": 26,
    #         "frozenRowCount": 1
    #       }
    #     },
    #   "data": [
    #     {"rowData": [
    #         {
    #         "values": [
    #         {"userEnteredValue": {"stringValue": "DATUM"},
    #           "effectiveValue": {"stringValue": "DATUM"},
    #           "formattedValue": "DATUM",
    #           "userEnteredFormat": {..},
    #           "effectiveFormat": {...}
    #         },{
    #           "userEnteredValue": {"stringValue": "Auftraggeber"},
    #           "effectiveValue": {"stringValue": "Auftraggeber"},
    #           "formattedValue": "Auftraggeber",
    #           "userEnteredFormat": {...},
    #           "effectiveFormat": {...}
    #         },
    #         ...
    sheetjson = json.loads(content)
    for sheet in sheetjson['sheets']:
        for idx,rowdata in enumerate(sheet['data']):
            row = rowdata['rowData']
            singleRow = []
            for cell in row['values']:
                singleRow.append(cell['formattedValue'])
            obj = {"sheetid":sheetid,"rownum":idx,"rowvalues":singleRow}
            result.append(obj)

  print(result)
  return result

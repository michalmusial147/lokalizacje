# przed użyciem:
# pip install xlsxwriter

import json
import http.client
import xlsxwriter as xlsxwriter

key = 'highway'
values = ['bus_stop', 'platform']


def getDataFromOverpass(key, value):
    connection = http.client.HTTPConnection('lz4.overpass-api.de')
    headers = {}
    request = ('[out:json][timeout:25];'
               'area[name="Warszawa"][boundary=administrative]->.searchArea;'
               '('
               'node["{0}"="{1}"](area.searchArea);'
               'way["{0}"="{1}"](area.searchArea);'
               'relation["{0}"="{1}"](area.searchArea);'
               ');'
               'out center;'
               ).format(key, value)
    request = request.format(key,  value)
    osmAddres = '/api/interpreter'
    connection.request('POST', osmAddres, request, headers)
    response = connection.getresponse()
    decodedResponse = response.read().decode()
    print(decodedResponse)
    responseJSON = json.loads(decodedResponse)
    elements = responseJSON['elements']
    workbook = xlsxwriter.Workbook( key + "_" + value + '.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, 'id')
    worksheet.write(0, 1, 'type')
    worksheet.write(0, 2, 'name')
    worksheet.write(0, 3, 'lat')
    worksheet.write(0, 4, 'lng')
    row = 1
    column = 0
    for element in elements:
        worksheet.write(row, 0, element['id'])
        worksheet.write(row, 1, element['tags'][key])
        if ('name' in element['tags']):
            worksheet.write(row, 2, element['tags']['name'])
        if ('center' in element):
            worksheet.write(row, 3, element['center']['lat'])
            worksheet.write(row, 4, element['center']['lon'])
        else:
            worksheet.write(row, 4, element['lat'])
            worksheet.write(row, 5, element['lon'])
        row = row + 1
    workbook.close()

for value in values:
    getDataFromOverpass(key, value)
# getDataFromOverpass('leisure', 'sport_centre')
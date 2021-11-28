# przed użyciem:
# pip install xlsxwriter

import json
import http.client
import xlsxwriter as xlsxwriter

key = 'education'
values = ['university', 'school', 'college', 'kindergarten', 'centre', 'facultative_school', 'exercise_area']

def getDataFromOverpass(key, value):
    connection = http.client.HTTPConnection('lz4.overpass-api.de')
    headers = {}
    request = "[out:json];area[name=\"Warszawa\"][boundary=administrative]->.searchArea;node[\"{0}\"=\"{1}\"](area.searchArea);out geom;".format(key,  value)
    osmAddres = '/api/interpreter'
    connection.request('POST', osmAddres, request, headers)
    response = connection.getresponse()
    decodedResponse = response.read().decode()
    print(decodedResponse)
    responseJSON = json.loads(decodedResponse)
    elements = responseJSON['elements']
    workbook = xlsxwriter.Workbook( key + "_" + value + '.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, 'type')
    worksheet.write(0, 1, 'name')
    worksheet.write(0, 2, 'lat')
    worksheet.write(0, 3, 'lng')
    row = 1
    column = 0
    for element in elements:
        worksheet.write(row, 0, element['tags']['amenity'])
        if ('name' in element['tags']):
            worksheet.write(row, 1, element['tags']['name'])
        worksheet.write(row, 2, element['lat'])
        worksheet.write(row, 3, element['lon'])
        row = row + 1
    workbook.close()

for value in values:
    getDataFromOverpass(key, value)

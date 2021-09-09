# przed użyciem:
# pip install xlsxwriter

import json
import http.client
import xlsxwriter as xlsxwriter

typ = input('Natalko podaj proszę typ obiektu: ')

# połączenie http ( narazie tylko "przygotowane" )
połączenie = http.client.HTTPConnection('lz4.overpass-api.de')

# to nieważne )
nagłówki_dla_serwera = {}  # domyślne puste

# tzw body żądania http ( http ma header i body, nagłówek i ciałko )
żądanie = ('[out:json];'
           'area[name="Warszawa"][boundary=administrative]->.searchArea;'
           'node["amenity"="school"](area.searchArea);'
           'out geom;')

# adres endpointa, python doklei go automatycznie do adresu połączenia
adres_endpointa = '/api/interpreter'

# uruchomienie żądania http
połączenie.request('POST', adres_endpointa, żądanie, nagłówki_dla_serwera)

# pobranie odpowiedzi http
response = połączenie.getresponse()

#  pobranie  body ciała http dodatkowo odkodowanie bajtów do stringa
decodedResponse = response.read().decode()

#  drukuje ciało do konsoli
print(decodedResponse)

#  pobranie i odkodowanie body ciała http
responseJSON = json.loads(decodedResponse)

#  elements to lista wszystkich wynikowych obiektów
#  będziemy ją formatować
elements = responseJSON['elements']

# Workbook() takes one, non-optional, argument
# which is the filename that we want to create.

#my mamy sparametryzowany typ bo go podaliśmy na samym początku z konsoli ;)
workbook = xlsxwriter.Workbook(typ+'.xlsx')

# The workbook object is then used to add new
# worksheet via the add_worksheet() method.
worksheet = workbook.add_worksheet()

worksheet.write(0, 0, 'type')
worksheet.write(0, 1, 'name')
worksheet.write(0, 2, 'lat')
worksheet.write(0, 3, 'lng')

row = 1
column = 0

#przerobienie elements z api w elements do gisu z wybranymi 4 polami
for element in elements:
    worksheet.write(row, 0, element['tags']['amenity'])
    if('name' in element['tags']):
     worksheet.write(row, 1, element['tags']['name'])
    worksheet.write(row, 2, element['lat'])
    worksheet.write(row, 3, element['lon'])
    row = row + 1
# Finally, close the Excel file
# via the close() method.
workbook.close()
import xlrd
import mysql.connector
import unicodedata
import urllib.request
import shutil
import ssl

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="faf",
  database="team4"
)
mycursor = mydb.cursor()
mycursor.execute("DROP TABLE IF EXISTS crime_rates")
mycursor.execute("CREATE TABLE IF NOT EXISTS crime_rates (crime_rate_id int NOT NULL AUTO_INCREMENT PRIMARY KEY, location VARCHAR(255), crime_type VARCHAR(255), number int)")

context = ssl._create_unverified_context()
with urllib.request.urlopen('https://date.gov.md/ro/system/files/resources/2019-12/noiembrie_11.xls', context=context) as response, open('data.xls', 'wb') as out_file:
    shutil.copyfileobj(response, out_file)

xl_workbook = xlrd.open_workbook('data.xls')
xl_sheet = xl_workbook.sheet_by_index(0)

for col_idx in range(1, xl_sheet.ncols):
    
    if xl_sheet.cell_type(2, col_idx) in (xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK):
        continue
    else:
        city = xl_sheet.cell_value(2, col_idx)
        city = unicodedata.normalize('NFD', city)
        city = ''.join(c for c in city if not unicodedata.combining(c))
        
    for row_idx in range(6, xl_sheet.nrows):
        if xl_sheet.cell_type(row_idx, col_idx) in (xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK):
            cell_obj = 0
        else:
            cell_obj = xl_sheet.cell_value(row_idx, col_idx)
        
        crime_type = xl_sheet.cell_value(row_idx, 0)
        if crime_type == 'T  O  T  A  L':
            crime_type = "TOTAL"
        elif crime_type in [' DIN      DECEDAT', ' ELE     TRAUMATIZAT', 'D I N  - GRAVE', 'E L E - MEDIE', 'DIN|-DE TRANSPORT', 'ELE|-AVERII PERSON.']:
            continue
        crime_type = unicodedata.normalize('NFD', crime_type)
        crime_type = ''.join(c for c in crime_type if not unicodedata.combining(c))

        mycursor.execute(f"INSERT INTO crime_rates(location, crime_type, number) VALUES('{city}', '{crime_type}', {int(cell_obj)})")
        
        print(f"{city}: {crime_type}: {cell_obj}")
mydb.commit()
mycursor.close()
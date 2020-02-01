import csv
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

mycursor.execute("DROP TABLE IF EXISTS apartments")
mycursor.execute("CREATE TABLE IF NOT EXISTS apartments (apartment_id int NOT NULL AUTO_INCREMENT PRIMARY KEY, location VARCHAR(255), price VARCHAR(255), phone VARCHAR(255))")

print("here1")
with open('Sol.csv') as csvfile:
    csv_data = csv.reader(csvfile)
    for location, price, phone in csv_data:
        location = unicodedata.normalize('NFD', location)
        location = ''.join(c for c in location if not unicodedata.combining(c))

        price = unicodedata.normalize('NFD', price)
        price = ''.join(c for c in price if not unicodedata.combining(c))

        print(f'INSERT INTO apartments(location, price, phone) VALUES("{location}", "{price}", "{phone}")')
        mycursor.execute(f'INSERT INTO apartments(location, price, phone) VALUES("{location}", "{price}", "{phone}")')
mydb.commit()
mycursor.close()
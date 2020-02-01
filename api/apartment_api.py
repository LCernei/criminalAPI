import flask
import mysql.connector
import json

app = flask.Flask(__name__)
app.config["DEBUG"] = True

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="faf",
  database="team4"
)
mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM apartments")
apartments = mycursor.fetchall()

apartments_list = []
for _, location, price, phone in apartments:
    apartments_list.append({"location":location, "price":price, "phone":phone})


@app.route('/', methods=['GET'])
def home():
    return json.dumps(apartments_list)

# @app.route('/<location>', methods=['GET'])
# def get_for_location(location):
#     location = location.upper()
#     if location in crime_rates_dict:
#         return crime_rates_dict[location.upper()]
#     else:
#         return '{"error": "Invalid location"}'

app.run(host='0.0.0.0', port=5050)
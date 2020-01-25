import flask
import mysql.connector

app = flask.Flask(__name__)
app.config["DEBUG"] = True

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="faf",
  database="team4"
)
mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM crime_rates")
crime_rates = mycursor.fetchall()

crime_rates_dict = {}
for id, location, crime_type, number in crime_rates:
    crime_rates_dict.setdefault(location, {}).update({crime_type: number})


@app.route('/', methods=['GET'])
def home():
    return crime_rates_dict

@app.route('/<location>', methods=['GET'])
def get_for_location(location):
    location = location.upper()
    if location in crime_rates_dict:
        return crime_rates_dict[location.upper()]
    else:
        return '{"error": "Invalid location"}'

app.run(host='0.0.0.0')
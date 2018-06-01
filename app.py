import requests
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'

db = SQLAlchemy(app)

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        new_city = request.form.get('city')
        
        if new_city:
            new_city_obj = City(name=new_city)

            db.session.add(new_city_obj)
            db.session.commit()

    cities = City.query.all()

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=271d1234d3f497eed5b1d80a07b3fcd1'

    weather_data = []

    for city in cities:

        r = requests.get(url.format(city.name)).json()

        weather = {
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }

        weather_data.append(weather)


    return render_template('weather.html', weather_data=weather_data)


@app.route('/', methods=['GET', 'POST'])
def indexm():
    if request.method == 'POST':
        new_city = request.form.get('dcity')

        if new_city:
            new_city_obj = City.query.filter_by(name=new_city).first()
            if new_city_obj: #  check if found in DB
                db.session.delete(new_city_obj)
                db.session.commit()

    cities = City.query.all()
if __name__ == '__main__':
    app.debug = True
    app.secret_key = '\xb0\xdb\x92P\x89\x12\xb0j\xfc9%)N\xd5\x8f\xfc\xa3\xcf\xecmn\xb9\xc0\xca'
    app.run()

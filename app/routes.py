from random import randint
from datetime import datetime, timedelta
from flask import jsonify, render_template, request, redirect, flash
from app import app, db
from .models import Forecast
from .forms import ForecastForm

CITIES = ['amsterdam', 'moscow']

class Week:
    def __init__(self, start):
        self.start = start.strftime('%d-%m-%y')
        self.end = (start + timedelta(days=7)).strftime('%d-%m-%y')
        self.week_days = self.get_weekdays(start)
    
    
    def get_weekdays(self, start):
        weekdays = []
        for i in range(8):
            weekdays.append((start + timedelta(days=i)).strftime('%d-%m-%y'))
        return weekdays
                
def get_weather_for_date(day):
    return randint(5, 15)


@app.route('/error')
def home():
    raise
    return None, 200

@app.route('/')
@app.route('/week')
def weather_week():
    week = Week(datetime.today())
    week_weather = {day: get_weather_for_date(day) for day in week.week_days}
    return render_template('week_overview.html', week=week, city='Amsterdam', week_weather=week_weather)

@app.route('/week/<city>')
def weather_in_city(city):
    if city in CITIES:
        week = Week(datetime.today())
        week_weather = {day: get_weather_for_date(day) for day in week.week_days}
        return render_template('week_overview.html', week=week, city=city, week_weather=week_weather)
    return render_template('404.html'), 404
    

@app.route('/your_city')
def weather_your_city():
    week = Week(datetime.today())
    return render_template('week_overview.html', week=week)

@app.route('/forecast', methods=['POST', 'GET'])
def forecast():
    forecast_form = ForecastForm()
    if request.method == 'POST':
        if forecast_form.validate_on_submit():
            city = request.form.get('city')
            date = request.form.get('date')
            date_format = datetime.strptime(date, '%d-%m-%y')
            forecast = Forecast(city=city, date=date, temperature=get_weather_for_date(date))
            db.session.add(forecast)
            db.session.commit()
            return redirect('/')
        error = "Form was not validated"
        return render_template('error.html',form=forecast_form,error = error)
        
    return render_template('add_forecast.html', form=forecast_form)

@app.route('/forecast/<_id>', methods=['GET', 'PATCH'])
def forecast_for_id(_id):
    if request.method == 'PATCH':
        temperature = request.args.get('temperature')
        
        forecast = Forecast.query.get_or_404(_id)
        forecast.temperature = temperature
        db.session.commit()
            
        return jsonify({'id':forecast._id}), 200
    elif request.method == 'GET':
        forecast = Forecast.query.get_or_404(_id)
        return jsonify({'id': forecast._id, 'city': forecast.city, 'temperature': forecast.temperature, 'date': forecast.date})


@app.route('/delete_forecast/<_id>', methods=['DELETE'])
def delete_forecast(_id):
    forecast = Forecast.query.get_or_404(_id)
    db.session.delete(forecast)
    db.commit()
    return jsonify({'result': True})
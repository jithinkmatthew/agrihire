from flask_wtf import FlaskForm
from wtforms import BooleanField


class WeatherForecast(FlaskForm):
    equipment_weather_forecast = BooleanField('Show weather forecast for this location')
    
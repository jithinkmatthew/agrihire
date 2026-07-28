from flask import Blueprint, request
from app.Utils import Utils
from app.controllers.auth.auth_controller import auth_required


weather = Blueprint('weather', __name__)

@weather.route('/weather', methods=['GET'])
@auth_required
def weather_forecast():
    
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    forecast_data = Utils.get_weather_forcast(lat, lon)
    
    return forecast_data

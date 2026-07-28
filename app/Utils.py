import datetime
import requests
from .config import Config
import os
from werkzeug.utils import secure_filename
from flask import flash
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

class Utils:
    @staticmethod
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS
    
    @staticmethod
    def upload_file(file, upload_folder, newname):
        try:
            if file and Utils.allowed_file(file.filename):
                filename = secure_filename(newname)
                os.makedirs(upload_folder, exist_ok=True)
                file_path = os.path.join(upload_folder, filename)
                file.save(file_path)
                return file_path
            else:
                return False
        except Exception as e:
            flash(f"Error uploading file: {e}")
            return False
        
    @staticmethod
    def get_weather_forcast(lat, lon):
    
        API_KEY = 'a73588d78ef0f94ed4581af9b1011911'    
        
        base_url = 'http://api.openweathermap.org/data/2.5/forecast'
        params = {
            'lat': lat,
            'lon': lon,
            'appid': API_KEY    
        }
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            return response.json()
        return None

class TimeUtils:
    
    @staticmethod
    def timeformat(time_str):
        """Convert 'HH:MM' string to 'HH:MM AM/PM' format"""
        time_obj = datetime.strptime(time_str, "%H:%M").time()
        return time_obj.strftime("%I:%M %p")
    
    @staticmethod
    def dateformat(date_value):
        if isinstance(date_value, date):  # already a date object
            return date_value.strftime("%d-%m-%Y")
        else:  # string
            date_obj = datetime.strptime(date_value, "%Y-%m-%d").date()
            return date_obj.strftime("%d-%m-%Y")
          
    @staticmethod
    def date_between(d1, d2):
        print("Called date_between with:", d1, d2)
        if not d1 or not d2:
            return ""
        diff = relativedelta(d2, d1)
        parts = []
        if diff.years:
            parts.append(f"{diff.years} year{'s' if diff.years != 1 else ''}")
        if diff.months:
            parts.append(f"{diff.months} month{'s' if diff.months != 1 else ''}")
        return ", ".join(parts)
class StatusFormatUtils:
    @staticmethod
    def format_status_filter(status_key):
        spaced_status = status_key.replace('_', ' ')
        return spaced_status.title()
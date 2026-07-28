from flask import flash
from app import db

class LocationRepository:
    
    @staticmethod
    def get_regions():
        try: 
            str_sql = """SELECT * FROM location_regions"""
            params = []

            with db.get_cursor() as cursor:
                cursor.execute(str_sql, params)
                return cursor.fetchall()
        except Exception as e:
            flash(f"Error retrieving regions: {e}")
            
    @staticmethod
    def get_districts(region_id):
        try: 
            str_sql = """SELECT * FROM location_districts WHERE region_id=%s """

            with db.get_cursor() as cursor:
                cursor.execute(str_sql, (region_id,))
                return cursor.fetchall()
        except Exception as e:
            flash(f"Error retrieving districts:  {e}")
        
    @staticmethod
    def get_suburbs(district_id):
        try: 
            str_sql = """SELECT * FROM location_suburbs WHERE district_id=%s """

            with db.get_cursor() as cursor:
                cursor.execute(str_sql, (district_id,))
                return cursor.fetchall()
        except Exception as e:
            flash(f"Error retrieving suburbs:  {e}")
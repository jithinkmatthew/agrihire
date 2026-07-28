
from flask import flash, session
from app import db

class DashboardRepository:

    @staticmethod
    def get_land_dashboard_details():
        try: 
            str_sql = """SELECT 
                        (SELECT COUNT(*) FROM land_parcels WHERE user_id = %s) AS total_land_parcels,
                        (SELECT COUNT(*) FROM land_parcels WHERE is_public = 1 AND user_id = %s) AS public_land_parcels,
                        (SELECT COUNT(*) FROM land_applications WHERE tenant_id = %s) AS requests_sent,
                        (SELECT COUNT(*) FROM land_applications la
                        INNER JOIN land_parcels lp ON la.land_parcel_id = lp.land_parcel_id
                        WHERE lp.user_id = %s) AS requests_received;"""
            params = []
            params.append(session['user_id'])
            params.append(session['user_id'])
            params.append(session['user_id'])
            params.append(session['user_id'])

            with db.get_cursor() as cursor:
                cursor.execute(str_sql, params)
                return cursor.fetchall()
        except Exception as e:
            flash(f"Error retrieving land dashboard details: {e}")
            return []
        
        
    @staticmethod
    def get_equipment_dashboard_details():
        try: 
            str_sql = """SELECT
                        (SELECT COUNT(*) FROM equipments WHERE user_id = %s) AS total_equipments,
                        (SELECT COUNT(*) FROM equipments WHERE is_public = 1 AND user_id = %s) AS public_equipments,
                        (SELECT COUNT(*) FROM equipment_requests 
                            WHERE hirer_user_id = %s) AS requests_sent,
                        (SELECT COUNT(*) FROM equipment_requests er
                        INNER JOIN equipments e ON er.equipment_id = e.equipment_id
                        WHERE e.user_id = %s) AS requests_received;"""
            params = []
            params.append(session['user_id'])
            params.append(session['user_id'])
            params.append(session['user_id'])
            params.append(session['user_id'])

            with db.get_cursor() as cursor:
                cursor.execute(str_sql, params)
                return cursor.fetchall()
        except Exception as e:
            flash(f"Error retrieving equipment dashboard details: {e}")
            return []



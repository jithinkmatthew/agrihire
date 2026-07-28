from flask import flash
from app import db

class UserRepository:
    
    @staticmethod
    def add_user(user_data):
        try:
            with db.get_cursor() as cursor:
                str_sql = '''INSERT INTO users (username, first_name, last_name, email, mobile, password_hash, location, profile_image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''
                params = []
                params.append(user_data['username'])
                params.append(user_data['first_name'])
                params.append(user_data['last_name'])
                params.append(user_data['email'])
                params.append(user_data.get('mobile', None))
                params.append(user_data['password_hash'])
                params.append(user_data.get('location', None))
                params.append(user_data.get('profile_image', None))
                
                cursor.execute(str_sql, params)
                return cursor.rowcount
        except Exception as e:
            flash(f"Error while adding new user: {e}")
            print(e)
            return -1
        
        
    @staticmethod
    def get_user(username=None, email=None, user_id=None):
        
        try: 
            str_sql = """SELECT * from users"""
            params = []

            if username:
                str_sql += " WHERE username = %s"
                params.append(username)
            elif email:
                str_sql += " WHERE email = %s"
                params.append(email)
            elif user_id:
                str_sql += " WHERE user_id = %s"
                params.append(user_id)                
            else:
                str_sql += " ORDER BY username"

            with db.get_cursor() as cursor:
                cursor.execute(str_sql, params)
                return cursor.fetchone() if len(params) == 1 else cursor.fetchall()
        except Exception as e:
            flash(f"Error retrieving user data: {e}")
            
    @staticmethod
    def update_user(user_id, update_data):
        
        try:
            str_sql = '''UPDATE users SET 
                        first_name = %s, last_name = %s, email = %s, 
                        mobile = %s, location = %s, profile_image = %s
                        WHERE user_id = %s'''
            params = []
            params.append(update_data['first_name'])
            params.append(update_data['last_name'])
            params.append(update_data['email'])
            params.append(update_data['mobile'])
            params.append(update_data['location']) if update_data['location'] else params.append(None)
            params.append(update_data['profile_image'])
            params.append(user_id)
            with db.get_cursor() as cursor:
                cursor.execute(str_sql, params)
                return cursor.rowcount
        except Exception as e:
            flash(f"Error updating user data: {e}")
            return -1

            
        
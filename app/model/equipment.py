from flask import flash
from app import db

class EquipmentRepository:
    
    @staticmethod
    def get_equipment_categories():
        try: 
            str_sql = """SELECT category_id, name from equipment_categories"""
            params = []

            with db.get_cursor() as cursor:
                cursor.execute(str_sql, params)
                return cursor.fetchall()
        except Exception as e:
            flash(f"Error retrieving equipment categories: {e}")
            return []
    
    @staticmethod
    def get_all_equipment_categories():
        try: 
            str_sql = """SELECT subcategory_id,name from equipment_subcategories"""
            params = []

            with db.get_cursor() as cursor:
                cursor.execute(str_sql, params)
                return cursor.fetchall()
        except Exception as e:
            flash(f"Error retrieving equipment categories: {e}")
            return []
                    
    @staticmethod
    def get_equipment_subcategories(category_id):
        try: 
            str_sql = """SELECT subcategory_id,name from equipment_subcategories WHERE category_id=%s"""

            with db.get_cursor() as cursor:
                cursor.execute(str_sql, (category_id,))
                return cursor.fetchall()
        except Exception as e:
            flash(f"Error retrieving equipment sub categories: {e}")
            return []
                        
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
            return []           
    
    @staticmethod
    def get_districts(region_id):
        try: 
            str_sql = """SELECT district_id,name FROM location_districts WHERE region_id = %s;"""
            params = []
            params.append(region_id)

            with db.get_cursor() as cursor:
                cursor.execute(str_sql, params)
                return cursor.fetchall()
        except Exception as e:
            flash(f"Error retrieving ditricts: {e}") 
            return []           
            
            
    @staticmethod
    def get_suburbs(district_id):
        try: 
            str_sql = """SELECT suburb_id,name FROM location_suburbs WHERE district_id = %s;"""
            params = []
            params.append(district_id)

            with db.get_cursor() as cursor:
                cursor.execute(str_sql, params)
                return cursor.fetchall()
        except Exception as e:
            flash(f"Error retrieving suburbs: {e}")    
            return []        
            
    @staticmethod
    def get_safety_options():
        try: 
            str_sql = """SELECT safety_id,name FROM safety_options;"""
            params = []

            with db.get_cursor() as cursor:
                cursor.execute(str_sql, params)
                return cursor.fetchall()
        except Exception as e:
            flash(f"Error retrieving safety_options: {e}")
            return []
    
    @staticmethod
    def add_equipment(equipment_data, uploaded_files, user_id):
        try:
            with db.get_cursor() as cursor:
                str_sql = '''INSERT INTO equipments (name, make, model, year, category_id, sub_category_id, 
                            user_id, description, price, price_modal, region_id, district_id, suburb_id, street_name,
                            city, zip, latitude, longitude, height, length, width, weight, is_public, is_hired, status)
                            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
                
                params = []
                params.append(equipment_data['equipment_name'])
                params.append(equipment_data['equipment_make'])
                params.append(equipment_data['equipment_model'])
                params.append(equipment_data['equipment_year'])
                params.append(equipment_data['equipment_category'])
                params.append(equipment_data['equipment_sub_category'])
                params.append(equipment_data['user_id'])
                params.append(equipment_data['equipment_description'])
                params.append(equipment_data['equipment_price'])
                params.append(equipment_data['equipment_price_modal'])
                params.append(equipment_data['location_region'])
                params.append(equipment_data['location_district'])
                params.append(equipment_data['location_suburbs'])
                params.append(equipment_data['location_street_name'])
                params.append(equipment_data['location_city'])
                params.append(equipment_data['location_zip'])
                
                lat, lon = map(float, equipment_data['location_gps_coordinate'].split(', '))
                params.append(lat)
                params.append(lon)
                
                params.append(equipment_data['equipment_height'])
                params.append(equipment_data['equipment_length'])
                params.append(equipment_data['equipment_width'])
                params.append(equipment_data['equipment_weight'])
                params.append(0)
                params.append(0)
                params.append('listed')
                
                cursor.execute(str_sql, params)
                equipment_id = cursor.lastrowid
                
                # Insert equipment safety details
                safety_ids = equipment_data.get('safety_equipments', [])
                if safety_ids:
                    values = [(equipment_id, sid) for sid in safety_ids]
                    cursor.executemany('''INSERT INTO equipment_safety_options (equipment_id, safety_id) VALUES(%s, %s)''', values)
                    
                safety_doc = uploaded_files.get('safety_docs')
                if safety_doc:
                    values = [(equipment_id, sdoc, 'safety_doc', user_id) for sdoc in safety_doc]
                    cursor.executemany('''INSERT INTO equipment_files (equipment_id, file_path, file_type, user_id) VALUES(%s, %s, %s, %s)''', values)
                
                safety_image = uploaded_files.get('equipment_image')
                if safety_image:
                    values = [(equipment_id, eqpimage, 'image', user_id) for eqpimage in safety_image]
                    cursor.executemany('''INSERT INTO equipment_files (equipment_id, file_path, file_type, user_id) VALUES(%s, %s, %s, %s)''', values)
                    
                return cursor.rowcount
            
        except Exception as e:
            flash(f"Error while adding new equipment: {e}")
            print(e)
            return -1

    @staticmethod
    def edit_equipment(update_data, equipment_id):
        
        try:
            # Map form keys to DB column names
            field_map = {
                "equipment_name": "name",
                "equipment_make": "make",
                "equipment_model": "model",
                "equipment_year": "year",
                "equipment_category_id": "category_id",
                "equipment_sub_category_id": "sub_category_id",
                "equipment_description": "description",
                "equipment_price": "price",
                "equipment_price_modal": "price_modal",
                "location_region_id": "region_id",
                "location_district_id": "district_id",
                "location_suburb_id": "suburb_id",
                "location_street_name": "street_name",
                "location_city": "city",
                "location_zip": "zip",
                "equipment_height": "height",
                "equipment_length": "length",
                "equipment_width": "width",
                "equipment_weight": "weight",
            }

            set_clauses = []
            params = []

            for form_field, db_column in field_map.items():
                if form_field in update_data and update_data[form_field] is not None:
                    set_clauses.append(f"{db_column} = %s")
                    params.append(update_data[form_field])

            # Handle GPS specially
            if "location_gps_coordinate" in update_data and update_data["location_gps_coordinate"]:
                lat, lon = map(float, update_data["location_gps_coordinate"].split(","))
                set_clauses.append("latitude = %s")
                set_clauses.append("longitude = %s")
                params.append(lat)
                params.append(lon)

            # Always update timestamp
            set_clauses.append("updated_date = CURRENT_TIMESTAMP")

            sql = f"UPDATE equipments SET {', '.join(set_clauses)} WHERE equipment_id = %s"
            params.append(equipment_id)

            print("SQL ----->", sql)
            print("Params -->", params)

            with db.get_cursor() as cursor:
                cursor.execute(sql, params)
                equip_table_count = cursor.rowcount
                # return cursor.rowcount
            
            # Track update rowcounts for files
            files_update_count = 0
            
            # Update Equipment Files Table for Image
            if "equipment_image" in update_data and update_data["equipment_image"]:
                
                str_sql = '''UPDATE equipment_files
                            SET file_path = %s
                            WHERE file_type = 'image'
                            AND equipment_id = %s'''
                
                params = []
                params.append(update_data["equipment_image"])
                params.append(equipment_id)
            
                with db.get_cursor() as cursor:
                    cursor.execute(str_sql, params)
                    files_update_count += cursor.rowcount
            
            # Update Equipment Files Table for Doc
            if "safety_docs" in update_data and update_data["safety_docs"]:
                
                str_sql = '''UPDATE equipment_files
                            SET file_path = %s
                            WHERE file_type = 'safety_doc'
                            AND equipment_id = %s'''
                
                params = []
                params.append(update_data["safety_docs"])
                params.append(equipment_id)
            
                with db.get_cursor() as cursor:
                    cursor.execute(str_sql, params)
                    files_update_count += cursor.rowcount
        
            return equip_table_count + files_update_count

        except Exception as e:
            flash(f"Error updating equipment data: {e}")
            return -1   
        
    @staticmethod
    def get_equipments(user_id):
        try: 
            str_sql = """SELECT e.equipment_id, e.name, 
                            e.make, e.model, e.year, e.user_id,
                            e.description,
                            e.price,
                            e.price_modal,
                            e.is_public,
                            e.is_hired,
                            e.status,
                            e.updated_date, e.height, 
                            e.length, e.width, e.weight,
                            c.name AS category_name,
                            sc.category_id AS sub_category_parent_id,
                            sc.name AS sub_category_name,
                            sc.subcategory_id AS sub_category_id,
                            lg.name AS region,
                            ld.region_id AS district_region_id,
                            ld.name AS district,
                            ls.district_id AS suburb_district_id,
                            ls.name AS suburb,
                            ls.suburb_id AS suburb_id,
                            e.street_name,
                            e.city,
                            e.zip,
                            e.latitude,
                            e.longitude
                            FROM equipments AS e
                            INNER JOIN equipment_categories AS c
                            ON e.category_id = c.category_id
                            INNER JOIN equipment_subcategories AS sc 
                            ON e.sub_category_id = sc.subcategory_id
                            INNER JOIN location_suburbs AS ls
                            ON e.suburb_id = ls.suburb_id
                            INNER JOIN location_districts as ld
                            ON e.district_id = ld.district_id
                            INNER JOIN location_regions as lg
                            ON e.region_id = lg.region_id
                            WHERE e.user_id=%s
                            ORDER BY e.equipment_id DESC"""
            params = []
            params.append(user_id)

            with db.get_cursor() as cursor:
                cursor.execute(str_sql, params)
                return cursor.fetchall()
        except Exception as e:
            flash(f"Error retrieving equipments: {e}")
            
    @staticmethod
    def get_equipment(equip_id):
        try: 
            str_sql = """SELECT e.equipment_id, e.name, 
                            e.make, e.model, e.year, e.user_id,
                            e.description,
                            e.price,
                            e.price_modal,
                            e.is_public,
                            e.is_hired,
                            e.status,
                            e.updated_date, e.height, 
                            e.length, e.width, e.weight,
                            c.name AS category_name,
                            sc.category_id AS sub_category_parent_id,
                            sc.name AS sub_category_name,
                            sc.subcategory_id AS sub_category_id,
                            lg.name AS region,
                            ld.region_id AS district_region_id,
                            ld.name AS district,
                            ls.district_id AS suburb_district_id,
                            ls.name AS suburb,
                            ls.suburb_id AS suburb_id,
                            e.street_name,
                            e.city,
                            e.zip,
                            e.latitude,
                            e.longitude
                            FROM equipments AS e
                            INNER JOIN equipment_categories AS c
                            ON e.category_id = c.category_id
                            INNER JOIN equipment_subcategories AS sc 
                            ON e.sub_category_id = sc.subcategory_id
                            INNER JOIN location_suburbs AS ls
                            ON e.suburb_id = ls.suburb_id
                            INNER JOIN location_districts as ld
                            ON e.district_id = ld.district_id
                            INNER JOIN location_regions as lg
                            ON e.region_id = lg.region_id
                            WHERE e.equipment_id=%s"""
            params = []
            params.append(equip_id)

            with db.get_cursor() as cursor:
                cursor.execute(str_sql, params)
                return cursor.fetchall()
        except Exception as e:
            flash(f"Error retrieving [equipment]: {e}") 
                       
    @staticmethod
    def get_equipments_files():
        try:
            str_sql = """SELECT equipment_id, file_id, file_path, file_type, uploaded_at
                         FROM equipment_files"""
            params = []
            # params = params
            with db.get_cursor() as cursor:
                cursor.execute(str_sql, params)
                return cursor.fetchall()
        except Exception as e:
            flash(f"Error retrieving [equipments] files: {e}")
            return False

    @staticmethod
    def get_equipment_files(equipment_ids):
        try: 
            if not equipment_ids:
                return []
            placeholders = ','.join(['%s'] * len(equipment_ids))
            str_sql = f"""SELECT equipment_id, file_id, file_path, file_type, uploaded_at
                         FROM equipment_files
                         WHERE equipment_id IN ({placeholders})"""
            # params = []
            # params = (tuple(equipment_ids),)
            with db.get_cursor() as cursor:
                cursor.execute(str_sql, equipment_ids)
                return cursor.fetchall()
        except Exception as e:
            flash(f"Error retrieving equipment files: {e}")
            return []
        
    @staticmethod
    def get_equipments_safety_options():
        try:
            str_sql = """SELECT eso.equipment_id, so.name
                        FROM equipment_safety_options AS eso
                        INNER JOIN safety_options AS so
                        ON eso.safety_id = so.safety_id"""
            params = []
            with db.get_cursor() as cursor:
                cursor.execute(str_sql, params)
                return cursor.fetchall()
        except Exception as e:
            flash(f"Error retrieving all equipments safety options: {e}")
            return []
        
    @staticmethod
    def get_equipment_safety_options(equip_id):
        try:
            str_sql = """SELECT eso.equipment_id, eso.safety_id, so.name
                        FROM equipment_safety_options AS eso
                        INNER JOIN safety_options AS so
                        ON eso.safety_id = so.safety_id
                        WHERE eso.equipment_id=%s"""
            params = []
            params.append(equip_id)
            with db.get_cursor() as cursor:
                cursor.execute(str_sql, params)
                return cursor.fetchall()
        except Exception as e:
            flash(f"Error retrieving [equipment] safety options: {e}")
            return []
                
    @staticmethod
    def delete_equipment(equip_id):
        try: 
            str_sql = """DELETE from equipments WHERE equipment_id=%s"""
            params = []
            params.append(equip_id)

            with db.get_cursor() as cursor:
                cursor.execute(str_sql, params)
                return cursor.rowcount > 0
        except Exception as e:
            flash(f"Error when deleting equipment: {e}")
            return False
    
    @staticmethod
    def publish_equipment(equip_id):
        try: 
            str_sql = """UPDATE equipments SET is_public=1 WHERE equipment_id=%s"""
            params = []
            params.append(equip_id)

            with db.get_cursor() as cursor:
                cursor.execute(str_sql, params)
                return cursor.rowcount > 0
        except Exception as e:
            flash(f"Error when publishing equipment: {e}")
            return False            
        
    @staticmethod
    def unpublish_equipment(equip_id):
        try: 
            str_sql = """UPDATE equipments SET is_public=0 WHERE equipment_id=%s"""
            params = []
            params.append(equip_id)

            with db.get_cursor() as cursor:
                cursor.execute(str_sql, params)
                return cursor.rowcount > 0
        except Exception as e:
            flash(f"Error when unpublishing equipment: {e}")
            return False

    @staticmethod
    def update_hired_status(status, equip_id):
        try: 
            str_sql = """UPDATE equipments SET is_hired=%s, is_public=0 WHERE equipment_id=%s"""
            params = []
            params.append(status)
            params.append(equip_id)

            with db.get_cursor() as cursor:
                cursor.execute(str_sql, params)
                return cursor.rowcount > 0
        except Exception as e:
            flash(f"Error when updating hired status: {e}")
            return False  
                
    @staticmethod
    def update_equipment_status(status, equip_id):
        try: 
            str_sql = """UPDATE equipments SET status=%s WHERE equipment_id=%s"""
            params = []
            params.append(status)
            params.append(equip_id)

            with db.get_cursor() as cursor:
                cursor.execute(str_sql, params)
                return cursor.rowcount > 0
        except Exception as e:
            flash(f"Error when updating equipment status: {e}")
            return False
    
    @staticmethod
    def get_equipment_request(equip_req_id):
        try:
            str_sql = """SELECT equipment_id, hirer_user_id, is_active from equipment_requests
                        WHERE request_id = %s"""
            params = []
            params.append(equip_req_id)
            with db.get_cursor() as cursor:
                cursor.execute(str_sql, params)
                return cursor.fetchall()
        except Exception as e:
            flash(f"Error retrieving [equipment_request]: {e}")
            return []
    
    @staticmethod
    def update_equipment_request_status(status, req_id):
        try: 
            str_sql = """UPDATE equipment_requests 
                        SET is_active = %s
                        WHERE request_id = %s"""
            params = []
            params.append(status)
            params.append(req_id)

            with db.get_cursor() as cursor:
                cursor.execute(str_sql, params)
                return cursor.rowcount > 0
        except Exception as e:
            flash(f"Error when updating equipment_request status: {e}")
            return False  
                
    @staticmethod
    def get_active_rentals_as_renter(user_id):
        try: 
            str_sql = """SELECT 
                        e.equipment_id,
                        e.name AS equipment_name,
                        e.make,
                        e.model,
                        e.year,
                        e.user_id AS owner_user_id,
                        e.price,
                        e.price_modal,
                        e.status AS equipment_status,
                        r.request_id,
                        r.hirer_user_id,
                        r.rental_start_date,
                        r.rental_end_date,
                        r.rental_start_time,
                        r.rental_end_time,
                        r.rental_rate,
                        r.rental_duration,
                        r.rental_delivery_amount,
                        r.is_active AS request_status,
                        r.created_at AS transaction_date,
                        t.transaction_id,
                        t.payment_mode,
                        t.transaction_amount FROM equipments e
                        INNER JOIN equipment_requests r 
                            ON e.equipment_id = r.equipment_id
                        INNER JOIN equipment_transactions t 
                            ON r.request_id = t.request_id
                        WHERE r.is_active=TRUE
                        AND r.hirer_user_id = %s"""
                        
            params = []
            params.append(user_id)

            with db.get_cursor() as cursor:
                cursor.execute(str_sql, params)
                return cursor.fetchall()
        except Exception as e:
            flash(f"Error when getting active equipment orders(renter) {e}")
            return []      

    @staticmethod
    def get_past_rentals_as_renter(user_id):
        try: 
            str_sql = """SELECT 
                        e.equipment_id,
                        e.name AS equipment_name,
                        e.make,
                        e.model,
                        e.year,
                        e.user_id AS owner_user_id,
                        e.price,
                        e.price_modal,
                        e.status AS equipment_status,
                        r.request_id,
                        r.hirer_user_id,
                        r.rental_start_date,
                        r.rental_end_date,
                        r.rental_start_time,
                        r.rental_end_time,
                        r.rental_rate,
                        r.rental_duration,
                        r.rental_delivery_amount,
                        r.is_active AS request_status,
                        r.created_at AS transaction_date,
                        t.transaction_id,
                        t.payment_mode,
                        t.transaction_amount FROM equipments e
                        INNER JOIN equipment_requests r 
                            ON e.equipment_id = r.equipment_id
                        INNER JOIN equipment_transactions t 
                            ON r.request_id = t.request_id
                        WHERE r.hirer_user_id = %s
                        AND r.is_active=0"""
                        
            params = []
            params.append(user_id)

            with db.get_cursor() as cursor:
                cursor.execute(str_sql, params)
                return cursor.fetchall()
        except Exception as e:
            flash(f"Error when getting past equipment orders(renter) {e}")
            return []
    
    @staticmethod
    def get_active_rentals_as_owner(user_id):
        try: 
            str_sql = """SELECT 
                        e.equipment_id,
                        e.name AS equipment_name,
                        e.make,
                        e.model,
                        e.year,
                        e.user_id AS owner_user_id,
                        e.price,
                        e.price_modal,
                        e.status AS equipment_status,
                        r.request_id,
                        r.hirer_user_id,
                        r.rental_start_date,
                        r.rental_end_date,
                        r.rental_start_time,
                        r.rental_end_time,
                        r.rental_rate,
                        r.rental_duration,
                        r.rental_delivery_amount,
                        r.rental_delivery_option,
                        r.rental_delivery_address,
                        r.is_active AS request_status,
                        r.created_at AS transaction_date,
                        t.transaction_id,
                        t.payment_mode,
                        t.transaction_amount FROM equipments e
                        INNER JOIN equipment_requests r 
                            ON e.equipment_id = r.equipment_id
                        INNER JOIN equipment_transactions t 
                            ON r.request_id = t.request_id
                        WHERE r.is_active = 1
                        AND e.user_id = %s;"""
            params = []
            params.append(user_id)

            with db.get_cursor() as cursor:
                cursor.execute(str_sql, params)
                return cursor.fetchall()
        except Exception as e:
            flash(f"Error when updating equipment status: {e}")
            return []

    @staticmethod
    def get_past_rentals_as_owner(user_id):
        try: 
            str_sql = """SELECT 
                        e.equipment_id,
                        e.name AS equipment_name,
                        e.make,
                        e.model,
                        e.year,
                        e.user_id AS owner_user_id,
                        e.price,
                        e.price_modal,
                        e.status AS equipment_status,
                        r.request_id,
                        r.hirer_user_id,
                        r.rental_start_date,
                        r.rental_end_date,
                        r.rental_start_time,
                        r.rental_end_time,
                        r.rental_rate,
                        r.rental_duration,
                        r.rental_delivery_amount,
                        r.rental_delivery_option,
                        r.rental_delivery_address,
                        r.is_active AS request_status,
                        r.created_at AS transaction_date,
                        t.transaction_id,
                        t.payment_mode,
                        t.transaction_amount FROM equipments e
                        INNER JOIN equipment_requests r 
                            ON e.equipment_id = r.equipment_id
                        INNER JOIN equipment_transactions t 
                            ON r.request_id = t.request_id
                        WHERE r.is_active=0
                        AND e.user_id = %s;"""
                        
            params = []
            params.append(user_id)

            with db.get_cursor() as cursor:
                cursor.execute(str_sql, params)
                return cursor.fetchall()
        except Exception as e:
            flash(f"Error when updating equipment status: {e}")
            return []
        

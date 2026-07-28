from flask import flash, session
from app import db

class LandRepository:
    
    @staticmethod
    def get_land_categories():
        try: 
            str_sql = """SELECT category_id, name from land_categories"""
            # land_categories
            params = []

            with db.get_cursor() as cursor:
                cursor.execute(str_sql, params)
                return cursor.fetchall()
        except Exception as e:
            flash(f"Error retrieving equipment categories: {e}")
            return []

    @staticmethod
    def add_land_parcel(land_parcel_data):
        try:
            with db.get_cursor() as cursor:
                str_sql = '''INSERT INTO land_parcels (name, description, category_id, region_id, district_id, suburb_id, street_name, city, zip,
                            latitude, longitude, size, rate, lease_modal, file_path, user_id, is_public, is_leased)
                            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''

                params = []
                params.append(land_parcel_data['land_parcel_name'])
                params.append(land_parcel_data['land_parcel_description'])
                params.append(land_parcel_data['land_parcel_category_id'])
                params.append(land_parcel_data['land_parcel_region_id'])
                params.append(land_parcel_data['land_parcel_district_id'])
                params.append(land_parcel_data['land_parcel_suburb_id'])
                params.append(land_parcel_data['land_parcel_street_name'])
                params.append(land_parcel_data['land_parcel_city'])
                params.append(land_parcel_data['land_parcel_zip'])
                lat, lon = map(float, land_parcel_data['location_gps_coordinate'].split(', '))
                params.append(lat)
                params.append(lon)
                params.append(land_parcel_data['land_parcel_size'])
                params.append(land_parcel_data['land_parcel_rate'])
                params.append(land_parcel_data['land_parcel_lease_modal'])
                params.append(land_parcel_data['land_parcel_image_path'])
                params.append(land_parcel_data['land_parcel_user_id'])
                params.append(0)
                params.append(0)
                
                cursor.execute(str_sql, params)
                # land_parcel_id = cursor.lastrowid
                            
                return cursor.rowcount
            
        except Exception as e:
            flash(f"Error while adding Land: {e}")
            print(e)
            return -1

    @staticmethod
    def get_land_parcels(user_id):
        try: 
            str_sql = """SELECT lp.land_parcel_id,
                                lp.name,
                                lp.description,
                                lc.name AS category_name,
                                lr.region_id,
                                lr.name AS region_name,
                                ld.district_id,
                                ld.name AS district_name,
                                ls.suburb_id,
                                ls.name AS suburb_name,
                                lp.street_name,
                                lp.city,
                                lp.zip,
                                lp.latitude,
                                lp.longitude,
                                lp.size,
                                lp.rate,
                                lp.lease_modal,
                                lp.file_path,
                                lp.user_id,
                                lp.is_public,
                                lp.is_leased,
                                lp.updated_date
                                FROM land_parcels lp
                                INNER JOIN land_categories lc ON lp.category_id = lc.category_id
                                INNER JOIN location_regions lr ON lp.region_id = lr.region_id
                                INNER JOIN location_districts ld ON lp.district_id = ld.district_id
                                INNER JOIN location_suburbs ls ON lp.suburb_id = ls.suburb_id
                                WHERE lp.user_id = %s
                                ORDER BY lp.updated_date DESC"""
            params = []
            params.append(user_id)

            with db.get_cursor() as cursor:
                cursor.execute(str_sql, params)
                return cursor.fetchall()
        except Exception as e:
            flash(f"Error retrieving land parcels: {e}")
         
    @staticmethod
    def get_land_parcel(parcel_id):
        try: 
            str_sql = """SELECT lp.land_parcel_id,
                                lp.name,
                                lp.description,
                                lc.category_id,
                                lc.name AS category_name,
                                lr.region_id,
                                lr.name AS region_name,
                                ld.district_id,
                                ld.name AS district_name,
                                ls.suburb_id,
                                ls.name AS suburb_name,
                                lp.street_name,
                                lp.city,
                                lp.zip,
                                lp.latitude,
                                lp.longitude,
                                lp.size,
                                lp.rate,
                                lp.lease_modal,
                                lp.file_path,
                                lp.user_id,
                                lp.is_public,
                                lp.is_leased,
                                lp.updated_date
                                FROM land_parcels lp
                                INNER JOIN land_categories lc ON lp.category_id = lc.category_id
                                INNER JOIN location_regions lr ON lp.region_id = lr.region_id
                                INNER JOIN location_districts ld ON lp.district_id = ld.district_id
                                INNER JOIN location_suburbs ls ON lp.suburb_id = ls.suburb_id
                                WHERE lp.land_parcel_id = %s """
            params = []
            params.append(parcel_id)

            with db.get_cursor() as cursor:
                cursor.execute(str_sql, params)
                return cursor.fetchall()
        except Exception as e:
            flash(f"Error retrieving [land parcel]: {e}")
   
    
    @staticmethod
    def delete_land_parcel(parcel_id):
        try: 
            str_sql = """DELETE from land_parcels WHERE land_parcel_id=%s"""
            params = []
            params.append(parcel_id)

            with db.get_cursor() as cursor:
                cursor.execute(str_sql, params)
                return cursor.rowcount > 0
        except Exception as e:
            flash(f"Error when deleting land parcel: {e}")
            return False
    
    @staticmethod
    def publish_land_parcel(parcel_id):
        try: 
            str_sql = """UPDATE land_parcels SET is_public=1 WHERE land_parcel_id=%s"""
            params = []
            params.append(parcel_id)
            print(str_sql, params)
            with db.get_cursor() as cursor:
                cursor.execute(str_sql, params)
                return cursor.rowcount > 0
        except Exception as e:
            flash(f"Error when publishing land parcel: {e}")
            return False            
        
    @staticmethod
    def unpublish_land_parcel(parcel_id):
        try: 
            str_sql = """UPDATE land_parcels SET is_public=0 WHERE land_parcel_id=%s"""
            params = []
            params.append(parcel_id)

            with db.get_cursor() as cursor:
                cursor.execute(str_sql, params)
                return cursor.rowcount > 0
        except Exception as e:
            flash(f"Error when unpublishing land parcel: {e}")
            return False
        
        
        
    @staticmethod
    def edit_land_parcel(update_data, parcel_id):
        
        try:
            # Map form keys to DB column names
            field_map = {
                "land_name": "name",
                "land_category": "category_id",
                "land_description": "description",
                "land_rate": "rate",
                "land_lease_modal": "lease_modal",
                "land_size": "size",
                "land_image": "file_path",
                "land_location_region": "region_id",
                "land_location_district": "district_id",
                "land_location_suburbs": "suburb_id",
                "land_location_street_name": "street_name",
                "land_location_city": "city",
                "land_location_zip": "zip"
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

            sql = f"UPDATE land_parcels SET {', '.join(set_clauses)} WHERE land_parcel_id = %s"
            params.append(parcel_id)
            
            print(sql, params)

            with db.get_cursor() as cursor:
                cursor.execute(sql, params)
                return cursor.rowcount

        except Exception as e:
            flash(f"Error updating land parcel data: {e}")
            return -1 
        
    @staticmethod
    def get_land_application_contact_details(parcel_req_id):
        try: 
            str_sql = """SELECT la.application_id,
                                lp.name AS land_parcel_name,
                                uo.first_name AS owner_first_name,
                                uo.last_name AS owner_last_name,
                                uo.email AS owner_email,
                                ut.first_name AS tenant_first_name,
                                ut.last_name AS tenant_last_name,
                                ut.email AS tenant_email
                                FROM land_applications la
                                INNER JOIN land_parcels lp ON la.land_parcel_id = lp.land_parcel_id
                                INNER JOIN users uo ON lp.user_id = uo.user_id
                                INNER JOIN users ut ON la.tenant_id = ut.user_id
                                WHERE la.application_id = %s"""
            params = []
            params.append(parcel_req_id)

            with db.get_cursor() as cursor:
                cursor.execute(str_sql, params)
                return cursor.fetchall()
        except Exception as e:
            flash(f"Error retrieving application contact details {e}")
        
    @staticmethod
    def submit_land_lease_application(application_data):
        
        connection = db.get_db()
        cursor = db.get_cursor()
        
        try:
            
            connection.start_transaction()
            
            # with db.get_cursor() as cursor:
            app_str_sql = '''INSERT INTO land_applications (land_parcel_id, tenant_id, status)
                        VALUES(%s, %s, %s);'''
            params = []
            params.append(application_data['land_parcel_id'])
            params.append(application_data['tenant_id'])
            params.append('pending')
            
            cursor.execute(app_str_sql, params)
            application_id = cursor.lastrowid
            
            if application_id:
                    
                str_sql = '''INSERT INTO land_application_details (application_id, farming_type, duration_years, experience, additional_notes)
                            VALUES (%s, %s, %s, %s, %s)'''
                
                details_param = []
                details_param.append(application_id)
                details_param.append(application_data['farming_type'])
                details_param.append(application_data['duration_years'])
                details_param.append(application_data['experience'])
                details_param.append(application_data['additional_notes'])
                
                cursor.execute(str_sql, details_param)
                
                log_sql = '''INSERT INTO land_application_log (`application_id`, `stage_number`, `stage_name`, `stage_status`, `created_by`, `completed_by`)
                            VALUES (%s, %s, %s, %s, %s, %s) '''
                
                log_params = []
                log_params.append(application_id)
                log_params.append(1)
                log_params.append('application')
                log_params.append('pending')
                log_params.append(session['user_id'])
                log_params.append(None)
                
                cursor.execute(log_sql, log_params)
                        
            connection.commit()
                
            return cursor.rowcount
            
        except Exception as e:
            connection.rollback()
            flash(f"Error while adding application request: {e}")
            print(e)
            return -1
        
    
    @staticmethod
    def get_land_parcel_requests_as_tenant():
        try: 
            str_sql = """SELECT la.application_id,
                                la.land_parcel_id,
                                la.tenant_id,
                                la.status AS application_status,
                                la.created_at,
                                lad.duration_years,
                                lad.experience,
                                lad.additional_notes,
                                lc.name AS farming_type_name,
                                lp.name AS land_parcel_name,
                                lp.file_path
                                FROM land_applications la
                                INNER JOIN  land_application_details lad 
                                ON la.application_id = lad.application_id
                                INNER JOIN land_categories lc 
                                ON lad.farming_type = lc.category_id
                                INNER JOIN land_parcels lp 
                                ON la.land_parcel_id = lp.land_parcel_id
                                WHERE la.tenant_id = %s
                                ORDER BY la.updated_at DESC;"""
            params = []
            params.append(session['user_id'])

            with db.get_cursor() as cursor:
                cursor.execute(str_sql, params)
                return cursor.fetchall()
        except Exception as e:
            flash(f"Error retrieving [land parcel requests]: {e}")
            
            
    @staticmethod
    def get_land_parcel_request_as_tenant(parcel_req_id):
        try: 
            str_sql = """SELECT la.application_id,
                                la.land_parcel_id,
                                la.tenant_id,
                                la.status AS application_status,
                                la.created_at,
                                lad.duration_years,
                                lad.experience,
                                lad.additional_notes,
                                lc.name AS farming_type_name,
                                lp.name AS land_parcel_name,
                                lp.file_path,
                                lp.is_leased
                                FROM land_applications la
                                INNER JOIN  land_application_details lad 
                                ON la.application_id = lad.application_id
                                INNER JOIN land_categories lc 
                                ON lad.farming_type = lc.category_id
                                INNER JOIN land_parcels lp 
                                ON la.land_parcel_id = lp.land_parcel_id
                                WHERE la.tenant_id = %s
                                AND la.application_id = %s
                                ORDER BY la.updated_at DESC;"""
            params = []
            params.append(session['user_id'])
            params.append(parcel_req_id)

            with db.get_cursor() as cursor:
                cursor.execute(str_sql, params)
                return cursor.fetchall()
        except Exception as e:
            flash(f"Error retrieving [land parcel request]: {e}")


    @staticmethod
    def get_already_submitted_parcel_request_status(parcel_req_id):
        try: 
            str_sql = """SELECT lp.land_parcel_id, 
                                lp.name, 
                                lp.description
                                FROM land_parcels lp
                                WHERE lp.land_parcel_id = %s
                                  AND lp.is_public = 1
                                  AND lp.is_leased = 0
                                  AND NOT EXISTS (
                                        SELECT 1
                                        FROM land_applications la
                                        WHERE la.land_parcel_id = lp.land_parcel_id
                                          AND la.tenant_id = %s
                                          AND la.status IN ('pending', 'approved'));"""
            params = []
            params.append(parcel_req_id)
            params.append(session['user_id'])

            with db.get_cursor() as cursor:
                cursor.execute(str_sql, params)
                return cursor.fetchall()
        except Exception as e:
            flash(f"Error retrieving [land parcel request]: {e}")


    @staticmethod
    def sent_signed_agreement_as_tenant(signed_agreement_data):
        try: 
            str_sql = """UPDATE land_agreement
                        SET signed_agreement_doc = %s, tenant_id = %s
                        WHERE application_id = %s """
            params = []
            params.append(signed_agreement_data['signed_doc'])
            params.append(signed_agreement_data['tenant_id'])
            params.append(signed_agreement_data['application_id'])
            
            print(str_sql, params)
            
            with db.get_cursor() as cursor:
                cursor.execute(str_sql, params)
                return cursor.rowcount > 0
        except Exception as e:
            flash(f"Error when updating land agreement(sent to land owner) : {e}")
            return False

    @staticmethod
    def get_land_parcel_requests_as_owner():
        try: 
            str_sql = """SELECT la.application_id,
                                la.land_parcel_id,
                                la.tenant_id,
                                la.status AS application_status,
                                la.created_at,
                                lad.duration_years,
                                lad.experience,
                                lad.additional_notes,
                                lc.name AS farming_type_name,
                                lp.name AS land_parcel_name,
                                lp.file_path,
                                tu.first_name AS tenant_first_name,
                                tu.last_name AS tenant_last_name,
                                tu.email AS tenant_email
                                FROM land_applications la
                                INNER JOIN  land_application_details lad 
                                ON la.application_id = lad.application_id
                                INNER JOIN land_categories lc 
                                ON lad.farming_type = lc.category_id
                                INNER JOIN land_parcels lp 
                                ON la.land_parcel_id = lp.land_parcel_id
                                INNER JOIN users tu
                                ON la.tenant_id = tu.user_id
                                WHERE lp.user_id = %s
                                ORDER BY la.updated_at DESC;"""
            params = []
            params.append(session['user_id'])

            with db.get_cursor() as cursor:
                cursor.execute(str_sql, params)
                return cursor.fetchall()
        except Exception as e:
            flash(f"Error retrieving [land parcel requests] as owner: {e}")
            
            
    @staticmethod
    def get_land_parcel_request_as_owner(parcel_req_id):
        try: 
            str_sql = """SELECT la.application_id,
                                la.land_parcel_id,
                                la.tenant_id,
                                la.status AS application_status,
                                la.created_at,
                                lad.duration_years,
                                lad.experience,
                                lad.additional_notes,
                                lc.name AS farming_type_name,
                                lp.land_parcel_id,
                                lp.name AS land_parcel_name,
                                lp.file_path,
                                lp.is_leased
                                FROM land_applications la
                                INNER JOIN  land_application_details lad 
                                ON la.application_id = lad.application_id
                                INNER JOIN land_categories lc 
                                ON lad.farming_type = lc.category_id
                                INNER JOIN land_parcels lp 
                                ON la.land_parcel_id = lp.land_parcel_id
                                WHERE lp.user_id = %s
                                AND la.application_id = %s
                                ORDER BY la.updated_at DESC;"""
            params = []
            params.append(session['user_id'])
            params.append(parcel_req_id)

            with db.get_cursor() as cursor:
                cursor.execute(str_sql, params)
                return cursor.fetchall()
        except Exception as e:
            flash(f"Error retrieving [land parcel request] as owner: {e}")  
            
    @staticmethod
    def application_stage_approval_as_owner(application_id):
        connection = db.get_db()
        cursor = db.get_cursor()
        
        try: 
            
            connection.start_transaction()
            
            update_sql = """UPDATE land_application_log set stage_status = 'approved', completed_by = %s
                        WHERE stage_number = 1
                        AND application_id = %s"""
            params = []
            params.append(session['user_id'])
            params.append(application_id)
            print(update_sql, params)
            
            insert_sql = '''INSERT INTO land_application_log (`application_id`, `stage_number`, `stage_name`, `stage_status`, `created_by`, `completed_by`)
                            VALUES (%s, %s, %s, %s, %s, %s) '''
                            
                            
            log_params = []
            log_params.append(application_id)
            log_params.append(2)
            log_params.append('site_inspection')
            log_params.append('pending')
            log_params.append(session['user_id'])
            log_params.append(None)
            
            with db.get_cursor() as cursor:
                cursor.execute(update_sql, params)
                cursor.execute(insert_sql, log_params)
                
                connection.commit()
                return cursor.rowcount > 0
            
        except Exception as e:
            connection.rollback()
            flash(f"Error when updating application stage - approval: {e}")
            return False
        
        
    @staticmethod
    def application_stage_rejection_as_owner(application_id):
        connection = db.get_db()
        cursor = db.get_cursor()
        
        try: 
            
            connection.start_transaction()
            
            update_sql = """UPDATE land_application_log set stage_status = 'rejected', completed_by = %s
                        WHERE stage_number = 1
                        AND application_id = %s"""
            params = []
            params.append(session['user_id'])
            params.append(application_id)
            print(update_sql, params)
            
            application_sql = '''UPDATE land_applications
                                SET status = 'declined'
                                WHERE application_id = %s'''
                            
                            
            application_params = []
            application_params.append(application_id)
            
            with db.get_cursor() as cursor:
                cursor.execute(update_sql, params)
                cursor.execute(application_sql, application_params)
                
                connection.commit()
                return cursor.rowcount > 0
            
        except Exception as e:
            connection.rollback()
            flash(f"Error when updating application stage - rejection : {e}")
            return False

    @staticmethod
    def get_land_request_stages(parcel_req_id):
        try: 
            str_sql = """SELECT lal.log_id,
                                lal.application_id,
                                lal.stage_number,
                                lal.stage_name,
                                lal.stage_status,
                                lal.created_by,
                                lal.completed_by,
                                lal.completed_at,
                                la.land_parcel_id,
                                la.tenant_id,
                                la.status AS application_status,
                                la.created_at AS application_created_at,
                                la.updated_at AS application_updated_at
                                FROM land_application_log lal
                                LEFT JOIN land_applications la
                                ON lal.application_id = la.application_id
                                WHERE lal.application_id = %s"""
            params = []
            params.append(parcel_req_id)

            with db.get_cursor() as cursor:
                cursor.execute(str_sql, params)
                return cursor.fetchall()
        except Exception as e:
            flash(f"Error retrieving land parcel request stages: {e}")
            

    @staticmethod
    def add_site_inspection_details(site_inspection_data):
        
        connection = db.get_db()
        cursor = db.get_cursor()
        
        try:
            
            connection.start_transaction()
            
            str_sql = '''INSERT INTO land_site_inspections (application_id, scheduled_date, scheduled_start_time, scheduled_end_time, inspector_notes, created_by)
                                VALUES (%s, %s, %s, %s, %s, %s);'''

            params = []
            params.append(site_inspection_data['application_id'])
            params.append(site_inspection_data['inspection_date'])
            params.append(site_inspection_data['inspection_start_time'])
            params.append(site_inspection_data['inspection_end_time'])
            params.append(None)
            params.append(site_inspection_data['created_by'])
            
            cursor.execute(str_sql, params)
            
            connection.commit()
                
            return cursor.rowcount
    
        except Exception as e:
            connection.rollback()
            flash(f"Error while adding site inspection details: {e}")
            print(e)
            return -1
        
    @staticmethod
    def get_site_inspection_details(parcel_req_id):
        try: 
            str_sql = """SELECT inspection_id,
                                application_id,
                                scheduled_date,
                                scheduled_start_time,
                                scheduled_end_time,
                                inspector_notes,
                                created_by,
                                created_at
                                FROM land_site_inspections
                                WHERE application_id = %s"""
            params = []
            params.append(parcel_req_id)

            with db.get_cursor() as cursor:
                cursor.execute(str_sql, params)
                return cursor.fetchall()
        except Exception as e:
            flash(f"Error retrieving site inspection details: {e}")
        
    @staticmethod
    def inspection_stage_approval_as_owner(inspection_data):
        connection = db.get_db()
        cursor = db.get_cursor()
        
        try: 
            
            connection.start_transaction()
            
            update_sql = """UPDATE land_site_inspections 
                            SET inspector_notes = %s
                            WHERE application_id = %s"""
            params = []
            params.append(inspection_data['inspection_note'])
            params.append(inspection_data['land_request_id'])
            
            print(update_sql, params)
            
            log_sql = """UPDATE land_application_log set stage_status = 'approved', completed_by = %s
                        WHERE stage_number = 2
                        AND application_id = %s"""
            log_params = []
            log_params.append(session['user_id'])
            log_params.append(inspection_data['land_request_id'])
            
            insert_sql = '''INSERT INTO land_application_log (`application_id`, `stage_number`, `stage_name`, `stage_status`, `created_by`, `completed_by`)
                            VALUES (%s, %s, %s, %s, %s, %s) '''
                            
                            
            doc_params = []
            doc_params.append(inspection_data['land_request_id'])
            doc_params.append(3)
            doc_params.append('document_verification')
            doc_params.append('pending')
            doc_params.append(session['user_id'])
            doc_params.append(None)
            
            with db.get_cursor() as cursor:
                cursor.execute(update_sql, params)
                cursor.execute(log_sql, log_params)
                cursor.execute(insert_sql, doc_params)
                
                connection.commit()
                return cursor.rowcount > 0
            
        except Exception as e:
            connection.rollback()
            flash(f"Error when updating inspection stage - approval: {e}")
            return False

    @staticmethod
    def inspection_stage_declined_as_owner(inspection_data):
        connection = db.get_db()
        cursor = db.get_cursor()
        
        try: 
            
            connection.start_transaction()
            
            update_sql = """UPDATE land_site_inspections 
                            SET inspector_notes = %s
                            WHERE application_id = %s"""
            params = []
            params.append(inspection_data['inspection_note'])
            params.append(inspection_data['land_request_id'])
            
            print(update_sql, params)
            
            log_sql = """UPDATE land_application_log set stage_status = 'rejected', completed_by = %s
                        WHERE stage_number = 2
                        AND application_id = %s"""
            log_params = []
            log_params.append(session['user_id'])
            log_params.append(inspection_data['land_request_id'])
            
            with db.get_cursor() as cursor:
                cursor.execute(update_sql, params)
                cursor.execute(log_sql, log_params)
                
                connection.commit()
                return cursor.rowcount > 0
            
        except Exception as e:
            connection.rollback()
            flash(f"Error when updating inspection stage - decline: {e}")
            return False        
        
    @staticmethod
    def document_verification_stage_file_upload_as_tenant(doc_verification_data):
        connection = db.get_db()
        cursor = db.get_cursor()
        
        try: 
            
            connection.start_transaction()
            
            data = [(doc_verification_data['application_id'], 'identity', doc_verification_data['identity_doc'], doc_verification_data['uploaded_by'], None),
                    (doc_verification_data['application_id'], 'finance', doc_verification_data['financial_doc'], doc_verification_data['uploaded_by'], None),
                    (doc_verification_data['application_id'], 'reference', doc_verification_data['farming_ref_doc'], doc_verification_data['uploaded_by'], None)]
            
            sql_query = '''INSERT INTO land_document_verification (application_id, document_type, file_path, uploaded_by, verified_by) 
                            VALUES(%s, %s, %s, %s, %s)'''
            
            with db.get_cursor() as cursor:
                cursor.executemany(sql_query, data)
                
                connection.commit()
                return cursor.rowcount > 0
            
        except Exception as e:
            connection.rollback()
            flash(f"Error when uploading document verification files: {e}")
            return False
                
    @staticmethod
    def get_document_verification_files(parcel_req_id):
        try: 
            str_sql = """SELECT document_id,
                            application_id,
                            document_type,
                            file_path,
                            uploaded_by,
                            verified_by,
                            uploaded_at,
                            verified_at
                            FROM land_document_verification
                            WHERE application_id = %s"""
            params = []
            params.append(parcel_req_id)

            with db.get_cursor() as cursor:
                cursor.execute(str_sql, params)
                return cursor.fetchall()
        except Exception as e:
            flash(f"Error retrieving verification document details: {e}")

                   
    @staticmethod
    def document_verification_approval_as_owner(application_id):
        connection = db.get_db()
        cursor = db.get_cursor()
        
        try: 
            
            connection.start_transaction()
            
            update_sql = """UPDATE land_application_log set stage_status = 'approved', completed_by = %s
                        WHERE stage_number = 3
                        AND application_id = %s"""
            params = []
            params.append(session['user_id'])
            params.append(application_id)
            print(update_sql, params)
            
            updatedoc_verify_sql = """UPDATE land_document_verification set verified_by=%s
                                        WHERE application_id = %s"""
            doc_params = []
            doc_params.append(session['user_id'])
            doc_params.append(application_id)
            print(updatedoc_verify_sql, doc_params)            
            
            insert_sql = '''INSERT INTO land_application_log (`application_id`, `stage_number`, `stage_name`, `stage_status`, `created_by`, `completed_by`)
                            VALUES (%s, %s, %s, %s, %s, %s) '''
                                     
            log_params = []
            log_params.append(application_id)
            log_params.append(4)
            log_params.append('agreement_signing')
            log_params.append('pending')
            log_params.append(session['user_id'])
            log_params.append(None)
            
            with db.get_cursor() as cursor:
                cursor.execute(update_sql, params)
                cursor.execute(updatedoc_verify_sql, doc_params)
                cursor.execute(insert_sql, log_params)
                
                connection.commit()
                return cursor.rowcount > 0
            
        except Exception as e:
            connection.rollback()
            flash(f"Error when updating document upload - approval: {e}")
            return False
        
        
    @staticmethod
    def sent_agreement_proposal_as_owner(proposal_data):
        try:
            with db.get_cursor() as cursor:
                str_sql = '''INSERT INTO land_agreement (application_id, tenant_id, lease_from, lease_to, rent, pricing_modal,
                                security_deposit, intended_use, notes, proposed_agreement_doc,
                                signed_agreement_doc, approved_by) 
                                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''

                params = []
                params.append(proposal_data['application_id'])
                params.append(proposal_data['tenant_id'])
                params.append(proposal_data['lease_from'])
                params.append(proposal_data['lease_to'])
                params.append(proposal_data['rent'])
                params.append(proposal_data['pricing_modal'])
                params.append(proposal_data['security_deposit'])
                params.append(proposal_data['intended_use'])
                params.append(proposal_data['notes'])
                params.append(proposal_data['proposal_doc'])
                params.append(None)
                params.append(None)
                
                cursor.execute(str_sql, params)
                            
                return cursor.rowcount
            
        except Exception as e:
            flash(f"Error while senting proposal as owner: {e}")
            print(e)
            return -1
        

    @staticmethod
    def get_agreement_proposal_details(parcel_req_id):
        try: 
            str_sql = """SELECT application_id, 
                                tenant_id, 
                                lease_from, 
                                lease_to, 
                                rent, 
                                pricing_modal,
                                security_deposit, 
                                intended_use, 
                                notes, 
                                proposed_agreement_doc,
                                signed_agreement_doc, 
                                approved_by
                            FROM land_agreement
                            WHERE application_id = %s"""
            params = []
            params.append(parcel_req_id)

            with db.get_cursor() as cursor:
                cursor.execute(str_sql, params)
                return cursor.fetchall()
        except Exception as e:
            flash(f"Error retrieving agreement proposal details: {e}")
            
            
    @staticmethod
    def initiate_lease_as_owner(lease_data):
        connection = db.get_db()
        cursor = db.get_cursor()
        
        try: 
            
            connection.start_transaction()
            
            # land_agreement
            agreement_sql = """UPDATE land_agreement
                                SET approved_by = %s
                                WHERE application_id = %s"""
            agreement_params = []
            agreement_params.append(session['user_id'])
            agreement_params.append(lease_data['application_id'])
            
            # land_application_log
            log_sql = """UPDATE land_application_log
                                SET stage_status = 'approved', completed_by = %s
                                WHERE application_id = %s"""
            log_params = []
            log_params.append(session['user_id'])
            log_params.append(lease_data['application_id'])
                                    
            # land_applications             
            application_sql = """UPDATE land_applications
                                SET status = 'approved'
                                WHERE application_id = %s"""
            application_params = []
            application_params.append(lease_data['application_id'])
            
            # land_parcel
            parcel_sql = """UPDATE land_parcels
                                    SET is_public = 0, is_leased = 1
                                    WHERE land_parcel_id = %s"""
            parcel_params = []
            parcel_params.append(lease_data['land_parcel_id'])
            
            with db.get_cursor() as cursor:
                cursor.execute(agreement_sql, agreement_params)
                cursor.execute(log_sql, log_params)
                cursor.execute(application_sql, application_params)
                cursor.execute(parcel_sql, parcel_params)
                
                connection.commit()
                return cursor.rowcount > 0
            
        except Exception as e:
            connection.rollback()
            flash(f"Error when updating Initiate Lease: {e}")
            return False

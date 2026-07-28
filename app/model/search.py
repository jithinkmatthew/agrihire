from flask import flash
from app import db

class SearchRepository:
    
    @staticmethod
    def find_equipments(search_fields):
        try: 
            print("search_fields", search_fields)
            str_sql = """SELECT e.equipment_id, e.name, 
                            e.make, e.model, e.year, e.user_id,
                            e.description,
                            e.price,
                            e.price_modal,
                            e.is_public,
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
                            e.longitude,
                            ef.file_path AS image_file
                            FROM equipments AS e
                            INNER JOIN equipment_categories AS c
                                ON e.category_id = c.category_id
                            INNER JOIN equipment_subcategories AS sc 
                                ON e.sub_category_id = sc.subcategory_id
                            INNER JOIN location_suburbs AS ls
                                ON e.suburb_id = ls.suburb_id
                            INNER JOIN location_districts AS ld
                                ON e.district_id = ld.district_id
                            INNER JOIN location_regions AS lg
                                ON e.region_id = lg.region_id
                            LEFT JOIN (
                                SELECT equipment_id, MIN(file_path) AS file_path
                                FROM equipment_files
                                WHERE file_type = 'image'
                                GROUP BY equipment_id
                            ) AS ef ON e.equipment_id = ef.equipment_id
                            WHERE e.is_public = 1
                              AND e.is_hired = 0
                              AND (e.user_id != %s)
                              AND (lg.region_id = %s OR %s = 0)
                              AND (ld.district_id = %s OR %s = 0)
                              AND (ls.suburb_id = %s OR %s = 0)
                              AND (c.category_id = %s OR %s = 0)
                            ORDER BY e.created_date DESC;"""
                            
            params = []
            params.append(search_fields.get('user_id_logged_in'))
            params.append(search_fields.get('region_id', 0))
            params.append(search_fields.get('region_id', 0))
            params.append(search_fields.get('district_id', 0))
            params.append(search_fields.get('district_id', 0))
            params.append(search_fields.get('suburb_id', 0))
            params.append(search_fields.get('suburb_id', 0))
            params.append(search_fields.get('category_id', 0))
            params.append(search_fields.get('category_id', 0))

            with db.get_cursor() as cursor:
                print('str_sql', str_sql)
                print('params', params)
                cursor.execute(str_sql, params)
                return cursor.fetchall()
        except Exception as e:
            flash(f"Error retrieving search result: {e}")
            
    @staticmethod
    def find_land_parcels(search_fields):
        try: 
            print("search_fields", search_fields)
            str_sql = """SELECT lp.land_parcel_id,
                                lp.name,
                                lp.description,
                                lc.name AS category_name,
                                lr.name AS region_name,
                                ld.name AS district_name,
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
                                WHERE lp.is_public = 1
                                AND lp.is_leased = 0
                                AND (lp.user_id != %s)
                                AND (lr.region_id = %s OR %s = 0)
                                AND (ld.district_id = %s OR %s = 0)
                                AND (ls.suburb_id = %s OR %s = 0)
                                AND (lc.category_id = %s OR %s = 0)
                                ORDER BY lp.created_date DESC;"""
            params = []
            params.append(search_fields.get('user_id_logged_in'))
            params.append(search_fields.get('region_id', 0))
            params.append(search_fields.get('region_id', 0))
            params.append(search_fields.get('district_id', 0))
            params.append(search_fields.get('district_id', 0))
            params.append(search_fields.get('suburb_id', 0))
            params.append(search_fields.get('suburb_id', 0))
            params.append(search_fields.get('category_id', 0))
            params.append(search_fields.get('category_id', 0))

            with db.get_cursor() as cursor:
                print('str_sql', str_sql)
                print('params', params)
                cursor.execute(str_sql, params)
                return cursor.fetchall()
        except Exception as e:
            flash(f"Error retrieving search result: {e}")
            
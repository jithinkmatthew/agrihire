

from flask import flash
from app import db
from app.model.equipment import EquipmentRepository


class OrderRepository:
    
    @staticmethod
    def process_order(order_data):
        try:
            with db.get_cursor() as cursor:
                sql_eqp = '''INSERT INTO equipment_requests ( `hirer_user_id`, `equipment_id`, `rental_start_date`, `rental_end_date`, `rental_start_time`, `rental_end_time`, 
                            `rental_rate`, `is_perday`, `is_perhour`, `rental_duration`, 
                            `rental_delivery_amount`, `rental_delivery_option`, `rental_delivery_address`, `is_active`) 
                            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
                            
                per_day = 1 if order_data.get('rental_duration_days') else 0
                per_hour = 1 if order_data.get('rental_duration_hours') else 0
                
                params = [
                    order_data.get('hirer_user_id'),
                    order_data.get('equip_id'),
                    order_data.get('rental_start_date'),
                    order_data.get('rental_end_date'),
                    order_data.get('rental_start_time'),
                    order_data.get('rental_end_time'),
                    order_data.get('rental_rate'),
                    per_day,
                    per_hour,
                    order_data.get('rental_duration_days') or order_data.get('rental_duration_hours'),
                    order_data.get('rental_delivery_amount'),
                    order_data.get('rental_delivery_option'),
                    order_data.get('rental_delivery_address'),
                    1
                ]
                
                cursor.execute(sql_eqp, params)
                request_id = cursor.lastrowid
                
                sql_trans = '''INSERT INTO equipment_transactions (`request_id`, `payment_mode`, `card_number`, 
                                `card_holder_name`, `card_expiration`, `card_cvv`, `transaction_amount`) 
                                VALUES(%s, %s, %s, %s, %s, %s, %s);'''
                
                params = [
                    request_id,
                    order_data.get('payment_mode'),
                    order_data.get('card_number'),
                    order_data.get('card_holder_name'),
                    order_data.get('card_exp'),
                    order_data.get('card_cvv'),
                    order_data.get('rental_grant_total')
                ]
                
                cursor.execute(sql_trans, params)
                
                # Updated Hired Status
                EquipmentRepository.update_hired_status(1, order_data.get('equip_id'))
                
                # Update Equipment Status
                EquipmentRepository.update_equipment_status('payment_completed', order_data.get('equip_id'))
                
                return cursor.rowcount 
            
        except Exception as e:
           flash(f"Error while processing equipment order: {e}")
           return -1
       
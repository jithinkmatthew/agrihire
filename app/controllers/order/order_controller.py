import os
import time
from flask import Blueprint, current_app, flash, redirect, render_template, request, session, url_for
from app.Utils import Utils
from app.controllers.auth.auth_controller import auth_required
from app.controllers.order.order_form import OrderForm, PaymentForm
from app.model.equipment import EquipmentRepository
from app.model.order import OrderRepository
from app.model.search import SearchRepository
from app.model.user import UserRepository


order = Blueprint('order', __name__)

@order.route('/equipment/<int:equip_id>/payment', methods=['GET', 'POST'])
@auth_required
def equipment_order_payment(equip_id):
    
    order_info = {}
    equipment = EquipmentRepository.get_equipment(equip_id)
    eq_id = [equip_id]
    equipment_files = EquipmentRepository.get_equipment_files(eq_id)
    print(equipment_files)
    
    orderform = OrderForm()
    paymentform = PaymentForm()
    
    
    # orderform.remove_required_validator('equipment_rental_end_date')
    
    if orderform.validate_on_submit():
        
        print("skills")
        print("equip_id" , equip_id)
        print(orderform.equipment_rental_start_date.data)
        order_info = { 
            "rental_start_date": orderform.equipment_rental_start_date.data.strftime('%Y-%m-%d'),
            "rental_end_date": orderform.equipment_rental_end_date.data.strftime('%Y-%m-%d') if orderform.equipment_rental_end_date.data else None,
            "rental_start_time": orderform.equipment_rental_start_time.data if orderform.equipment_rental_start_time.data else None,
            "rental_end_time": orderform.equipment_rental_end_time.data if orderform.equipment_rental_end_time.data else None,    
            "rental_delivery_option": orderform.equipment_delivery_option.data,
            "rental_delivery_address": orderform.equipment_site_address.data if orderform.equipment_site_address.data else None,
            "rental_duration_days": int(orderform.equipment_rental_days.data) if orderform.equipment_rental_days.data else None,
            "rental_duration_hours": float(orderform.equipment_rental_hours.data) if orderform.equipment_rental_hours.data else None,
            "rental_rate": int(orderform.equipment_rental_rate.data),
            "rental_delivery_amount": int(orderform.equipment_delivery_amount.data),
            "rental_grant_total": orderform.equipment_rental_grant_total.data 
        }
        
        session['order_info'] = order_info
        print("session['order_info']", session['order_info'])
        
    else: 
        flash('Something went wrong. Please try again !!', 'warning')
        return redirect(url_for('equipment.view_equipment', equip_id=equip_id))
        
    
    return render_template('order/payment.html', 
                           orderform=orderform,
                           paymentform=paymentform,
                           equipment = equipment,
                           equipment_files=equipment_files,
                           order_info=order_info)
    
@order.route('/equipment/<int:equip_id>/ordersummary', methods=['GET', 'POST'])
@auth_required
def equipment_order_confirmation(equip_id):
    
    try:
        equipment = EquipmentRepository.get_equipment(equip_id)

        # orderform = OrderForm()
        paymentform = PaymentForm()
    
        if paymentform.validate_on_submit():
        
            order_info = session['order_info']
        
            if not order_info:
                flash("No order information found. Please start your order again.", "warning")
                return redirect(url_for('equipment.view_equipment', equip_id=equip_id))
        
            order_info.update({
                "payment_mode": paymentform.payment_mode.data,
                "card_number": paymentform.card_number.data,
                "card_holder_name": paymentform.card_holder_name.data,
                "card_exp": paymentform.card_exp_date.data,
                "card_cvv": paymentform.card_cvv.data,
                "hirer_user_id": session['user_id'],
                "equip_id": equip_id
            })

            session['order_info'] = order_info
        
        
            result = OrderRepository.process_order(order_info)
            
            
            
            # OrderRepository.process_order(order_info)
            
            print('equipment_order_summary', result)
            if result > 0:
                session.pop('order_info', None)
                return redirect(url_for('order.equipment_order_confirmation', equip_id=equip_id))
            else:
                flash("Failed to complete the order. Please try again.", "danger")
                return redirect(url_for('equipment.view_equipment', equip_id=equip_id))
                        
    except Exception as e:
        # Handle unexpected errors
        flash(f"An unexpected error occurred: {str(e)}", "danger")

    return render_template('order/summary.html',
                           paymentform=paymentform,
                           equipment=equipment)
    

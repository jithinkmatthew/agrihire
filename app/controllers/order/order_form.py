from datetime import date
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import BooleanField, IntegerField, RadioField, StringField, SubmitField, SelectField, TextAreaField, SelectMultipleField, DateField, TimeField, widgets
from wtforms.validators import DataRequired, Email, InputRequired, Regexp, Length, Optional

class OrderForm(FlaskForm):
    today_str = date.today().strftime('%Y-%m-%d')
    time_slots = [("", "Please select time")] + [(f"{h:02d}:{m:02d}", f"{h}:{m:02d}") for h in range(7, 18) for m in (0, 30)]
    
    equipment_rental_start_time = SelectField('Start Time', choices=time_slots, validate_choice=False)
    equipment_rental_end_time = SelectField('End Time', choices=time_slots, validate_choice=False)

    equipment_rental_start_date = DateField('Rental Start Date', format='%Y-%m-%d', validators=[DataRequired()], render_kw={"min": today_str})
    equipment_rental_end_date = DateField('Rental End Date', format='%Y-%m-%d', render_kw={"min": today_str})
    
    # delivery service
    equipment_delivery_option = RadioField(
        'Delivery Method',
        choices=[('pickup', 'Pickup up'), ('address', 'Delivery to Address')],
        default='pickup',
        validators=[InputRequired()])
    equipment_site_address = StringField('Equipment Site Location')

    equipment_rental_days = StringField('Rental Days')
    equipment_rental_hours = StringField('Rental Hours')
    equipment_rental_rate = StringField('Rental Rate')
    equipment_delivery_amount = StringField('Delivey')
    equipment_rental_grant_total = StringField('Total')
    equipment_payment_btn = SubmitField('Payment')
    
    def remove_required_validator(self, field_name):
        field = getattr(self, field_name)
        field.validators = [v for v in field.validators if not isinstance(v, DataRequired)]
class PaymentForm(FlaskForm):

    payment_mode = RadioField('Credit Card', choices=[('credit', 'Credit'),('debit', 'Debit')], default='credit')
    card_number = StringField(
        'Card Number',
        validators=[
            DataRequired(message="Card Number is required"),
            Length(min=13, max=16, message="Card number must be between 13 and 16 digits"),
            Regexp('^[0-9]{13,16}$', message="Card number must contain only digits")
        ],
        render_kw={"placeholder": "Enter card number"})
    card_holder_name = StringField('Name on card')
    card_exp_date = StringField('Expiry date')
    card_cvv = IntegerField('CVV Code')
    place_order_btn = SubmitField('Place Order')
    
    
    
    

    
    
    
    

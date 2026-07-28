from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import HiddenField, StringField, SubmitField, SelectField, TextAreaField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Email

class EquipmentForm(FlaskForm):
    
    # Basic information
    equipment_name = StringField('Name*', validators=[DataRequired()])
    equipment_make = StringField('Equipment Make*', validators=[DataRequired()])
    equipment_model = StringField('Equipment Model*', validators=[DataRequired()])
    equipment_year = StringField('Equipment Make Year*', validators=[DataRequired()])
    equipment_category = SelectField('Equipment Category*', choices=[], validators=[DataRequired()], validate_choice=False, coerce=int)
    equipment_sub_category = SelectField('Equipment Sub Category*', choices=[], validators=[DataRequired()], validate_choice=False, coerce=int)
    equipment_description = TextAreaField('Description*', validators=[DataRequired()])
    # Price
    equipment_price = StringField('Price*', validators=[DataRequired()])
    equipment_price_modal = SelectField('PricingModal*', choices=[('per_hour', 'Per Hour'),('per_day', 'Per Day')], validators=[DataRequired()], validate_choice=False)
    
    
    # Location
    location_region = SelectField('Region*', choices=[], validators=[DataRequired()],validate_choice=False, coerce=int)
    location_district = SelectField('District*', choices=[], validators=[DataRequired()], validate_choice=False, coerce=int)
    location_suburbs = SelectField('Suburbs*', choices=[], validators=[DataRequired()], validate_choice=False, coerce=int)
    location_street_name = StringField('Street Name')
    location_city = StringField('City')
    location_zip = StringField('ZIP')
    location_gps_coordinate = StringField('GPS Coordinates*')
    location_get_coordinates_btn = SubmitField('Get GPS Coordinates')
    # Specifications
    equipment_height = StringField('Equipment Height(cm)*')
    equipment_length = StringField('Equipment Length(cm)*')
    equipment_width = StringField('Equipment Width(cm)*')
    equipment_weight = StringField('Equipment Weight(kg)*')
    # Safety
    safety_equipments = SelectMultipleField("Recommended Equipments",
        choices=[],
        option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(prefix_label=False),
        coerce=int)
    safety_docs = FileField('Safety Docs', validators=[FileAllowed(['pdf'], 'PDF only!')])
    # Equipment Image
    equipment_image = FileField('Equipment Image', validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    add_equipment_btn = SubmitField('Add Equipment')

class DeleteEquipmentForm(FlaskForm):
    submit = SubmitField('Delete')
class PublishEquipmentForm(FlaskForm):
    submit = SubmitField('Publish')
    
class UnPublishEquipmentForm(FlaskForm):
    submit = SubmitField('UnPublish')
    
class ManageEquipmentRequestForm(FlaskForm):
    equipment_status = SelectField('Request Status ', 
                                   choices=[('', 'Select status'),
                                            ('ready_for_pickup', 'Ready For PickUp'),
                                            ('in_use', 'In Use'),
                                            ('returned', 'Returned'),
                                            ('listed', 'Move to Draft')], 
                                   validators=[DataRequired()],
                                   validate_choice=False)
    update_status_btn = SubmitField('Update Status')
    
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import HiddenField, StringField, SubmitField, SelectField, TextAreaField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Email
from wtforms import SelectMultipleField, widgets

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class EquipmentSearchForm(FlaskForm):
    
    equipment_category = SelectField('Category', choices=[], validate_choice=False, coerce=int)
    equipment_region = SelectField('Region', choices=[], validate_choice=False, coerce=int)
    equipment_district = SelectField('District', choices=[], validate_choice=False, coerce=int)
    equipment_suburb = SelectField('Suburb', choices=[], validate_choice=False, coerce=int)
    equipment_search_btn = SubmitField('Search')
    
class LandSearchForm(FlaskForm):
    
    land_category = SelectField('Category', choices=[], validate_choice=False, coerce=int)
    land_region = SelectField('Region', choices=[], validate_choice=False, coerce=int)
    land_district = SelectField('District', choices=[], validate_choice=False, coerce=int)
    land_suburb = SelectField('Suburb', choices=[], validate_choice=False, coerce=int)
    land_search_btn = SubmitField('Search')
    

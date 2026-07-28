from datetime import date
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import DateField, DateTimeLocalField, DecimalField, FieldList, FormField, HiddenField, SelectField, StringField, SubmitField, TextAreaField, TimeField
from wtforms.validators import Regexp, DataRequired, InputRequired


class LandForm(FlaskForm):
    
    # Basic information
    land_name = StringField('Name*', validators=[DataRequired()])
    land_category = SelectField('Category*', choices=[], validators=[DataRequired()], validate_choice=False, coerce=int)
    land_description = TextAreaField('Description*', validators=[DataRequired()])
    land_location_region = SelectField('Region*', choices=[], validators=[DataRequired()],validate_choice=False, coerce=int)
    land_location_district = SelectField('District*', choices=[], validators=[DataRequired()], validate_choice=False, coerce=int)
    land_location_suburbs = SelectField('Suburbs*', choices=[], validators=[DataRequired()], validate_choice=False, coerce=int)
    land_location_street_name = StringField('Street Name')
    land_location_city = StringField('City')
    land_location_zip = StringField('ZIP')
    land_location_gps_coordinate = StringField('GPS Coordinates*', validators=[InputRequired()])
    land_location_get_coordinates_btn = SubmitField('Get GPS Coordinates')
    land_rate = DecimalField('Price*', validators=[DataRequired()])
    land_lease_modal = SelectField('PricingModal', choices=[('per_month', 'Per Month'),('per_year', 'Per Year')], validators=[DataRequired()], validate_choice=False)
    land_size = DecimalField('Land Size(Hectares)*', validators=[DataRequired()])
    land_image = FileField('Land Image', validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    add_land_btn = SubmitField('Add Land')

class DeleteLandForm(FlaskForm):
    submit = SubmitField('Delete')
    
class PublishLandForm(FlaskForm):
    submit = SubmitField('Publish')
    
class UnpublishLandForm(FlaskForm):
    submit = SubmitField('UnPublish')
    
class LandRequestForm(FlaskForm):
    
    land_intended_use = SelectField('Intended Use', 
                                              choices=[], 
                                              validators=[DataRequired()], 
                                              validate_choice=False)
    land_desired_lease_duration = SelectField('Desired Lease Duration', 
                                              choices=[('1', '1 Year'),('2', '2 Year'), ('3', '3 Year'),('0', 'Other')], 
                                              validators=[DataRequired()], 
                                              validate_choice=False)
    land_farming_experience = TextAreaField('Farming Experience', validators=[DataRequired()])
    land_additional_experience = TextAreaField('Additional Information', validators=[DataRequired()])
    land_application_submit_btn = SubmitField('Submit Application')
    

class LandApplicationStageForm(FlaskForm):
    land_application_stage_approve_btn = SubmitField('Approve & Continue')
    land_application_stage_decline_btn = SubmitField('Decline')
    
# class DateTimeEntryForm(FlaskForm):
#     datetime = DateTimeLocalField('Date and Time', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])    
    
class LandInspectionInviteForm(FlaskForm):
    today_str = date.today().strftime('%Y-%m-%d')
    land_inspection_date = DateField('Inspection Date', format='%Y-%m-%d', validators=[DataRequired()], render_kw={"min": today_str})
    land_inspection_start_time = TimeField('Select Start Time:', format='%H:%M', validators=[DataRequired()])
    land_inspection_end_time = TimeField('Select End Time:', format='%H:%M', validators=[DataRequired()])
    land_inspection_sent_invitation_btn = SubmitField('Sent Invitation')
    
class LandInspectionConfirmationForm(FlaskForm):
    
    land_inspection_note = TextAreaField('Note', validators=[DataRequired()])
    land_inspection_approval_btn = SubmitField('Approve & Continue')
    land_inspection_decline_btn = SubmitField('Decline')
    
class LandDocVerificationUploadForm(FlaskForm):
    land_verification_identity_doc = FileField('Identity Docs', validators=[FileRequired(message='Please upload your identity document.'), FileAllowed(['pdf'], 'PDF only!')])
    land_verification_financial_doc = FileField('Financial Statements', validators=[FileRequired(message='Please upload your Financial Statements.'), FileAllowed(['pdf'], 'PDF only!')])
    land_verification_farming_ref_doc = FileField('Farming Reference', validators=[FileRequired(message='Please upload your Farming Reference.'), FileAllowed(['pdf'], 'PDF only!')])
    land_doc_verification_submit_btn = SubmitField('Submit Documents')
    
class LandDocVerificationApproveForm(FlaskForm):   
    land_doc_verification_approve_btn = SubmitField('Submit Documents')
    land_doc_verification_reject_btn = SubmitField('Submit Documents')
    
class LandAgreementProposalForm(FlaskForm):   
    # land_agreement_lease_period = StringField('Lease Period', validators=[DataRequired()])
    today_str = date.today().strftime('%Y-%m-%d')
    land_agreement_lease_from_date = DateField('Lease From', format='%Y-%m-%d', validators=[DataRequired()], render_kw={"min": today_str})
    land_agreement_lease_to_date = DateField('Lease To', format='%Y-%m-%d', validators=[DataRequired()], render_kw={"min": today_str})
    land_agreement_rent = StringField('Rent', validators=[DataRequired()])
    land_agreement_modal = SelectField('PricingModal', choices=[('per_month', 'Per Month'),('per_year', 'Per Year')], validators=[DataRequired()], validate_choice=False)
    land_agreement_security = StringField('Security Deposite', validators=[DataRequired()])
    land_agreement_intended_use = SelectField('Intended Use', 
                                              choices=[], 
                                              validators=[DataRequired()], 
                                              validate_choice=False)
    land_agreement_notes = TextAreaField('Additional Notes', validators=[DataRequired()])
    land_agreement_proposal_doc = FileField('Agreement Proposal Document', validators=[FileAllowed(['pdf'], 'PDF only!')])
    land_agreement_proposal_btn = SubmitField('Sent Agreement to Tenant')
    
class LandAgreementSignForm(FlaskForm):
    land_agreement_sign_doc = FileField('Agreement Sign Document', validators=[FileAllowed(['pdf'], 'PDF only!')])
    land_agreement_proposal_btn = SubmitField('Sent Agreement to Owner')
    
class LandFinalApprovalForm(FlaskForm):
    land_request_final_approval_btn = SubmitField('Initiate Lease')
    
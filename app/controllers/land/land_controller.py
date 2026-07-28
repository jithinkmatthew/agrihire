import os
import time
from flask import Blueprint, abort, current_app, flash, redirect, render_template, request, session, url_for

from app.Utils import Utils
from app.controllers.auth.auth_controller import auth_required
from app.controllers.land.land_form import DeleteLandForm, LandAgreementProposalForm, LandAgreementSignForm, LandDocVerificationApproveForm, LandFinalApprovalForm, LandForm, LandRequestForm, LandApplicationStageForm, LandDocVerificationUploadForm, LandInspectionConfirmationForm, LandInspectionInviteForm, PublishLandForm, UnpublishLandForm
from app.model.equipment import EquipmentRepository
from app.model.land import LandRepository
from app.model.location import LocationRepository
from app.model.user import UserRepository

land = Blueprint('land', __name__)

class LandObjWrapper:
    def __init__(self, land_data):
        
        self.land_name = land_data.get('name')
        self.land_category = land_data.get('category_name')
        self.land_description = land_data.get('description')
        self.land_location_region = land_data.get('region_name')
        self.land_location_district = land_data.get('district_name')
        self.land_location_suburbs = land_data.get('suburb_name')
        self.land_location_street_name = land_data.get('street_name')
        self.land_location_city = land_data.get('city')
        self.land_location_zip = land_data.get('zip')
        self.land_location_gps_coordinate = f"{land_data.get('latitude')}, {land_data.get('longitude')}"
        self.land_rate = land_data.get('rate')
        self.land_lease_modal = land_data.get('lease_modal')
        self.land_size = land_data.get('size')
        self.land_image = land_data.get('file_path')

@land.route('/land/manage/add', methods=['GET', 'POST'])
@auth_required
def add_land_parcels():
    
    land_form = LandForm()
    land_parcel_data = {}
    
    if land_form.validate_on_submit():
                
        land_parcel_data = {
            'land_parcel_name' : land_form.land_name.data,
            'land_parcel_description' : land_form.land_description.data,
            'land_parcel_category_id' : land_form.land_category.data,
            'land_parcel_region_id' : land_form.land_location_region.data,
            'land_parcel_district_id' : land_form.land_location_district.data,
            'land_parcel_suburb_id' : land_form.land_location_suburbs.data,
            'land_parcel_suburb_id' : land_form.land_location_suburbs.data,
            'land_parcel_street_name' : land_form.land_location_street_name.data,
            'land_parcel_city' : land_form.land_location_city.data,
            'land_parcel_zip' : land_form.land_location_zip.data,
            'location_gps_coordinate' : land_form.land_location_gps_coordinate.data,
            'land_parcel_size' : land_form.land_size.data,
            'land_parcel_rate' : land_form.land_rate.data,
            'land_parcel_lease_modal' : land_form.land_lease_modal.data,
            'land_parcel_image_path' : land_form.land_image.data,
            'land_parcel_user_id' : session['user_id']
            }
        
        land_image = land_form.land_image.data
        
        if land_image and land_image.filename:
            
            # Save the file
            ext = os.path.splitext(land_image.filename)[1]
            # newname = f"{user['user_id']}equipimage{ext}"
            newname = f"{session['user_id']}image{int(time.time())}{ext}"
            upload_folder = os.path.join(current_app.static_folder, current_app.config['UPLOAD_FOLDER_LAND'], 'images')
            result = Utils.upload_file(land_image, upload_folder, newname)
            
            if result:
                print("Land Parcel image uploaded")
            else:
                print("Land Parcel image uploading failed")
            
            equipment_image_path=f"{current_app.config['UPLOAD_FOLDER_LAND']}/images/{newname}"
            
            land_parcel_data.update({
                'land_parcel_image_path': equipment_image_path
            })
        
        result = LandRepository.add_land_parcel(land_parcel_data)
            
        if result > 0:
            flash('🚀 Ready to go! Give it a quick check and publish to go live.', 'success')
            
        return redirect(url_for('land.manage_land_request'))
        
    return redirect(url_for('land.manage_land_request'))

@land.route('/land/manage/<int:parcel_id>/delete', methods=['POST'])
@auth_required
def delete_land_parcel(parcel_id):
    try:
        
        result = LandRepository.delete_land_parcel(parcel_id)
        if not result:
            flash('Land Parcel not found or could not be deleted.', 'warning')
        else:
            flash('Land Parcel deleted successfully.', 'success')
    except Exception as e:
        flash('An error occurred while deleting Land Parcel.', 'danger')
    
    # Redirect back to the referring URL
    redirect_url = request.referrer or url_for('land.manage_land_request')
    return redirect(redirect_url)

@land.route('/land/manage/<int:parcel_id>/publish', methods=['POST'])
@auth_required
def publish_land_parcel(parcel_id):
    try:
        
        result = LandRepository.publish_land_parcel(parcel_id)
        if not result:
            flash('Land Parcel could not be published.', 'warning')
        else:
            flash('Land Parcel published successfully.', 'success')
    except Exception as e:
        flash('An error occurred while publishing Land Parcel.', 'danger')
    
    # Redirect back to the referring URL
    redirect_url = request.referrer or url_for('land.manage_land_request')
    return redirect(redirect_url)

@land.route('/land/manage/<int:parcel_id>/unpublish', methods=['POST'])
@auth_required
def unpublish_land_parcel(parcel_id):
    try:
        
        result = LandRepository.unpublish_land_parcel(parcel_id)
        if not result:
            flash('Land Parcel could not be Unpublished.', 'warning')
        else:
            flash('Land Parcel Unpublished successfully.', 'success')
    except Exception as e:
        flash('An error occurred while Unpublishing Land Parcel.', 'danger')
    
    # Redirect back to the referring URL
    redirect_url = request.referrer or url_for('land.manage_land_request')
    return redirect(redirect_url)


@land.route('/land/manage', methods=['GET'])
@auth_required
def manage_land_request():
    
    # form = EquipmentForm()
    land_form = LandForm()
    publish_form = PublishLandForm()
    delete_form = DeleteLandForm()
    unpublish_form = UnpublishLandForm()
    
    categories = LandRepository.get_land_categories()
    category_choices = [(int(cat['category_id']), cat['name']) for cat in categories]
    land_form.land_category.choices = category_choices
    
    edit_land_form = {}
    land_parcels = LandRepository.get_land_parcels(session['user_id'])
    edit_form = None
    
    for land in land_parcels:
        
        land_obj = LandObjWrapper(land)
        edit_form = LandForm(obj=land_obj)
        
        categories = LandRepository.get_land_categories()
        category_choices = [(int(cat['category_id']), cat['name']) for cat in categories]
        edit_form.land_category.choices = category_choices
        # find matching category_id by name
        selected_cat_id = next((int(cat['category_id']) for cat in categories if cat['name'] == land_obj.land_category), None)
        edit_form.land_category.data = selected_cat_id
        
        regions = EquipmentRepository.get_regions();
        region_choices = [(reg['region_id'], reg['name']) for reg in regions]
        edit_form.land_location_region.choices = region_choices
        selected_reg_id = next((int(reg['region_id']) for reg in regions if reg['name'] == land_obj.land_location_region), None)
        edit_form.land_location_region.data = selected_reg_id
        
        districts = EquipmentRepository.get_districts(selected_reg_id)
        district_choices = [(dist['district_id'], dist['name']) for dist in districts]
        edit_form.land_location_district.choices = district_choices
        selected_dist_id = next((int(dist['district_id']) for dist in districts if dist['name'] == land_obj.land_location_district), None)
        edit_form.land_location_district.data = selected_dist_id
        
        suburbs = EquipmentRepository.get_suburbs(selected_dist_id)
        suburb_choices = [(sub['suburb_id'], sub['name']) for sub in suburbs]
        edit_form.land_location_suburbs.choices = suburb_choices
        selected_sub_id = next((int(sub['suburb_id']) for sub in suburbs if sub['name'] == land_obj.land_location_suburbs), None)
        edit_form.land_location_suburbs.data = selected_sub_id
        
        edit_land_form[land['land_parcel_id']] = edit_form

    return render_template('land/manage_land_listing.html', 
                           land_form=land_form,
                           edit_land_form=edit_land_form,
                           land_parcels=land_parcels,
                           publish_form=publish_form,
                           delete_form=delete_form,
                           unpublish_form=unpublish_form)

@land.route('/land/manage/<int:parcel_id>/edit', methods=['GET', 'POST'])
@auth_required
def edit_land_parcel(parcel_id):
    
    original_land_parcel = LandRepository.get_land_parcel(parcel_id)
    equipment_obj = LandObjWrapper(original_land_parcel[0])
    
    # Instantiate form, passing POST data only if it is a POST request, else pass obj for pre-filled form
    if request.method == 'POST':
        edit_land_form = LandForm(request.form)
    else:
        edit_land_form = LandForm(obj=equipment_obj)

    # For GET, set select field current values from equipment_obj
    if request.method == 'GET':
        # edit_form.equipment_category.data = equipment_obj.equipment_sub_category_parent_id
        # edit_form.equipment_sub_category.data = equipment_obj.equipment_sub_category_id
        # edit_form.location_region.data = equipment_obj.location_region
        # edit_form.location_district.data = equipment_obj.location_district
        # edit_form.location_suburbs.data = equipment_obj.location_suburbs
        print("Hi- get")
        # edit_form.safety_docs.data = [ item['file_path'] for item in equipment_files if item['file_type'] == 'safety_doc' ]
        

    if edit_land_form.validate_on_submit():
        
        changed_data = {}

        # Compare fields, add any changed data to changed_data dict
        if edit_land_form.land_name.data != original_land_parcel[0]['name']:
            changed_data['land_name'] = edit_land_form.land_name.data
        
        if edit_land_form.land_category.data != original_land_parcel[0]['category_id']:            
            categories = LandRepository.get_land_categories()
            # selected_cat_name = next((cat['name'] for cat in categories if cat['category_id'] == edit_land_form.land_category.data), None)
            changed_data['land_category'] = edit_land_form.land_category.data

        if edit_land_form.land_description.data != original_land_parcel[0]['description']:
            changed_data['land_description'] = edit_land_form.land_name.data            
            
        if edit_land_form.land_rate.data != original_land_parcel[0]['rate']:
            changed_data['land_rate'] = edit_land_form.land_rate.data                    
            
        if edit_land_form.land_lease_modal.data != original_land_parcel[0]['lease_modal']:
            changed_data['land_lease_modal'] = edit_land_form.land_lease_modal.data
            
        if edit_land_form.land_size.data != original_land_parcel[0]['size']:
            changed_data['land_size'] = edit_land_form.land_size.data                        
            
        if edit_land_form.land_location_region.data != original_land_parcel[0]['region_id']:
            changed_data['land_location_region'] = edit_land_form.land_location_region.data            
            
        if edit_land_form.land_location_district.data != original_land_parcel[0]['district_id']:
            changed_data['land_location_district'] = edit_land_form.land_location_district.data                        

        if edit_land_form.land_location_suburbs.data != original_land_parcel[0]['suburb_id']:
            changed_data['land_location_suburbs'] = edit_land_form.land_location_suburbs.data                        
            
        if edit_land_form.land_location_street_name.data != original_land_parcel[0]['street_name']:
            changed_data['land_location_street_name'] = edit_land_form.land_location_street_name.data                        
            
        if edit_land_form.land_location_city.data != original_land_parcel[0]['city']:
            changed_data['land_location_city'] = edit_land_form.land_location_city.data                        
                        
        if edit_land_form.land_location_zip.data != original_land_parcel[0]['zip']:
            changed_data['land_location_zip'] = edit_land_form.land_location_zip.data                        
            
        if edit_land_form.land_location_gps_coordinate.data != f"{original_land_parcel[0]['latitude']}, {original_land_parcel[0]['longitude']}":
            changed_data['location_gps_coordinate'] = edit_land_form.land_location_gps_coordinate.data            

        # Safety Docs
        uploaded_image = request.files.get('land_image')
        if uploaded_image and uploaded_image.filename:
            ext = os.path.splitext(uploaded_image.filename)[1]
            # newname = f"{user['user_id']}safetydoc{ext}"
            newname = f"{session['user_id']}img{int(time.time())}{ext}"
            upload_folder = os.path.join(current_app.static_folder, current_app.config['UPLOAD_FOLDER_LAND'], 'images')
            # remove existing file
            existing_image_filename = original_land_parcel[0]['file_path']
            
            if existing_image_filename:

                # Construct full path
                existing_image_location = os.path.join(
                    current_app.static_folder,
                    existing_image_filename  # assuming file_path is relative to static folder
                )
                
                if os.path.exists(existing_image_location):
                    os.remove(existing_image_location)
                    
            result = Utils.upload_file(uploaded_image, upload_folder, newname)

            if result:
                changed_data['land_image'] = os.path.join(current_app.config['UPLOAD_FOLDER_LAND'], 'images', newname)        
        
        if changed_data:            
            result = LandRepository.edit_land_parcel(changed_data, parcel_id)
            
            if result > 0:
                flash('Changes saved! Please publish to the public.', 'success')
            return redirect(url_for('land.manage_land_request'))
        
        else:
            flash("No changes were made.", "danger")

    # Render the edit equipment page with the form and equipment object
    return redirect(url_for('land.manage_land_request'))

@land.route('/land/<int:parcel_id>', methods=['GET'])
@auth_required
def view_land_parcel(parcel_id):
    try:
        
        # if 'username' not in session:
        #     return redirect(url_for('auth.login'))
        
        
        land = LandRepository.get_land_parcel(parcel_id)
        
        land_form = LandForm()
        land_application_form = LandRequestForm()
        
        land_parcel_categories = LandRepository.get_land_categories()
        category_choices = [(int(cat['category_id']), cat['name']) for cat in land_parcel_categories]
        land_application_form.land_intended_use.choices = [('', 'Please Select Intended Use')] + category_choices
        
        already_applied_status = LandRepository.get_already_submitted_parcel_request_status(parcel_id)
        
        # the data
        
    except Exception as e:
        flash('An error occurred while viewing equipment.', 'danger')
    
    return render_template('land/view_land.html', 
                           land_form=land_form,
                           land_application_form=land_application_form,
                           land=land,
                           already_applied_status=already_applied_status)
    
        
@land.route('/land/<int:parcel_id>/application/summary', methods=['GET', 'POST'])
@auth_required
def submit_land_parcel_request(parcel_id):
    try:
        
        land = LandRepository.get_land_parcel(parcel_id)
        land_application_form = LandRequestForm()
        
        application_data = {}
        
        if land_application_form.validate_on_submit():
            
            print("Do something")
            
            # use_type = land_application_form.land_intended_use.data
            # usage_value = dict(land_application_form.land_intended_use).choices.get(use_type)
            
            application_data.update({
                'land_parcel_id' : parcel_id,
                'tenant_id' : session['user_id'],
                'farming_type' : land_application_form.land_intended_use.data,
                'duration_years' : land_application_form.land_desired_lease_duration.data,
                'experience' : land_application_form.land_farming_experience.data,
                'additional_notes': land_application_form.land_additional_experience.data
            });
            
            result = LandRepository.submit_land_lease_application(application_data)
            
            if result > 0:
                return render_template('land/application_summary.html')
            else:
                flash("Something went wrong", "danger")
                return redirect(url_for('land.view_land_parcel', parcel_id=parcel_id))
            
    except Exception as e:
        flash('An error occurred while processing the application.', 'danger')
    
    return redirect(url_for('land.view_land_parcel', parcel_id=parcel_id))
        

@land.route('/land/request/outgoing', methods=['GET', 'POST'])
@auth_required
def view_land_requests_as_tenant():
    
    active_request_as_tenant = LandRepository.get_land_parcel_requests_as_tenant()
    
    return render_template('land/my_land_request.html',
                           active_request_as_tenant=active_request_as_tenant)
    

@land.route('/land/request/outgoing/<int:parcel_req_id>', methods=['GET', 'POST'])
@auth_required
def view_land_request_as_tenant(parcel_req_id):
    
    application_stage_form = LandApplicationStageForm()
    inspection_stage_form = LandInspectionInviteForm()
    inspection_confirm_form = LandInspectionConfirmationForm()
    document_verification_form = LandDocVerificationUploadForm()
    agreement_sign_form = LandAgreementSignForm()
    
    active_request_tenant = LandRepository.get_land_parcel_request_as_tenant(parcel_req_id)
    if not active_request_tenant:
        abort(404)
    
    contact_details = LandRepository.get_land_application_contact_details(parcel_req_id)
    parcel_req_stages = LandRepository.get_land_request_stages(parcel_req_id)
    site_inspection_data = LandRepository.get_site_inspection_details(parcel_req_id)
    verification_docs = LandRepository.get_document_verification_files(parcel_req_id)
    all_verified = all(doc['verified_by'] is not None for doc in verification_docs)
    proposal_data = LandRepository.get_agreement_proposal_details(parcel_req_id)
    
    
    return render_template('land/view_land_application_tenant.html',
                           application_stage_form=application_stage_form,
                           inspection_stage_form=inspection_stage_form,
                           inspection_confirm_form=inspection_confirm_form,
                           document_verification_form=document_verification_form,
                           agreement_sign_form=agreement_sign_form,
                           active_request_tenant=active_request_tenant,
                           contact_details=contact_details,
                           parcel_req_stages=parcel_req_stages,
                           site_inspection_data=site_inspection_data,
                           verification_docs=verification_docs,
                           all_verified=all_verified,
                           proposal_data=proposal_data)


@land.route('/land/request/outgoing/<int:parcel_req_id>/verification', methods=['GET', 'POST'])
@auth_required
def submit_document_for_verification_as_tenant(parcel_req_id):
    
    try:
        
        doc_verification_data = {}
        document_verification_form = LandDocVerificationUploadForm()
        
        if document_verification_form.validate_on_submit():
            
            identity_doc = document_verification_form and document_verification_form.land_verification_identity_doc.data
            financial_doc = document_verification_form and document_verification_form.land_verification_financial_doc.data
            farming_ref_doc = document_verification_form and document_verification_form.land_verification_farming_ref_doc.data

            if identity_doc:
            
                # Save the file
                ext = os.path.splitext(identity_doc.filename)[1]
                newname = f"{session['user_id']}idendoc{int(time.time())}{ext}"

                upload_folder = os.path.join(current_app.static_folder, current_app.config['UPLOAD_FOLDER_LAND'], 'docs')
                result = Utils.upload_file(identity_doc, upload_folder, newname)

                if result:
                    print("Identity doc uploaded")
                else:
                    print("Identity doc uploading failed")

                identity_doc_path=f"{current_app.config['UPLOAD_FOLDER_LAND']}/docs/{newname}"

                doc_verification_data.update({
                    'identity_doc': identity_doc_path
                })
                
            if financial_doc:
                
                # Save the file
                ext = os.path.splitext(financial_doc.filename)[1]
                newname = f"{session['user_id']}findoc{int(time.time())}{ext}"

                upload_folder = os.path.join(current_app.static_folder, current_app.config['UPLOAD_FOLDER_LAND'], 'docs')
                result = Utils.upload_file(financial_doc, upload_folder, newname)

                if result:
                    print("Financial Doc uploaded")
                else:
                    print("Financial Doc uploading failed")

                fin_doc_path=f"{current_app.config['UPLOAD_FOLDER_LAND']}/docs/{newname}"

                doc_verification_data.update({
                    'financial_doc': fin_doc_path
                })
            
            if farming_ref_doc:
                
                # Save the file
                ext = os.path.splitext(farming_ref_doc.filename)[1]
                newname = f"{session['user_id']}farmdoc{int(time.time())}{ext}"

                upload_folder = os.path.join(current_app.static_folder, current_app.config['UPLOAD_FOLDER_LAND'], 'docs')
                result = Utils.upload_file(farming_ref_doc, upload_folder, newname)

                if result:
                    print("Farming Reference uploaded")
                else:
                    print("Farming Reference uploading failed")

                fin_doc_path=f"{current_app.config['UPLOAD_FOLDER_LAND']}/docs/{newname}"

                doc_verification_data.update({
                    'farming_ref_doc': fin_doc_path
                })                                
            
            
            doc_verification_data.update({
                'application_id' : parcel_req_id,
                'uploaded_by' : session['user_id']
            })
            
            result = LandRepository.document_verification_stage_file_upload_as_tenant(doc_verification_data)
    
            if not result:
                flash('Something went wrong', 'warning')
            else:
                flash('Document uploaded successfully for verification', 'success')
            
            pass                      
        
        else:
            
            if document_verification_form.errors:
                flash('Something went wrong while uploading document. Please upload only pdf files', 'danger')
                            
    except Exception as e:
        flash('An error occurred while uploading document request.', 'danger')
    
    # Redirect back to the referring URL
    redirect_url = request.referrer or url_for('land.view_land_request_as_tenant')
    return redirect(redirect_url)

@land.route('/land/request/incoming/<int:parcel_req_id>/agreement/sent', methods=['GET', 'POST'])
@auth_required
def submit_signed_agreement_as_tenant(parcel_req_id):
    
    try:
        
        agreement_sign_form = LandAgreementSignForm()
        agreement_sign_data = {}
        
        if agreement_sign_form.validate_on_submit():
            
            agreement_sign_data.update({
                'application_id' : parcel_req_id,
                'tenant_id' : session['user_id']
            })
            
            agreement_sign_doc = agreement_sign_form and agreement_sign_form.land_agreement_sign_doc.data

            if agreement_sign_doc:
            
                # Save the file
                ext = os.path.splitext(agreement_sign_doc.filename)[1]
                newname = f"{session['user_id']}signed{int(time.time())}{ext}"

                upload_folder = os.path.join(current_app.static_folder, current_app.config['UPLOAD_FOLDER_LAND'], 'docs/signed')
                result = Utils.upload_file(agreement_sign_doc, upload_folder, newname)

                if result:
                    print("Signed Agreement doc uploaded")
                else:
                    print("Signed Agreement doc uploading failed")

                signed_doc_path=f"{current_app.config['UPLOAD_FOLDER_LAND']}/docs/signed/{newname}"

                agreement_sign_data.update({
                    'signed_doc': signed_doc_path
                })
            
            result = LandRepository.sent_signed_agreement_as_tenant(agreement_sign_data)
        
            if not result:
                flash('Something went wrong', 'warning')
            else:
                flash('The signed document has been sent to the landowner. ', 'success')
    except Exception as e:
        flash('An error occurred while Approving request.', 'danger')
    
    # Redirect back to the referring URL
    redirect_url = request.referrer or url_for('land.view_land_request_as_tenant')
    return redirect(redirect_url)

    
@land.route('/land/request/incoming', methods=['GET', 'POST'])
@auth_required
def view_land_requests_as_owner():
    
    active_requests_as_owner = LandRepository.get_land_parcel_requests_as_owner()
    
    return render_template('land/incoming_land_request.html',
                           active_requests_as_owner=active_requests_as_owner)
    
    
@land.route('/land/request/incoming/<int:parcel_req_id>', methods=['GET', 'POST'])
@auth_required
def view_land_request_as_owner(parcel_req_id):
    
    application_stage_form = LandApplicationStageForm()
    inspection_stage_form = LandInspectionInviteForm()
    inspection_confirm_form = LandInspectionConfirmationForm()
    doc_verification_form = LandDocVerificationApproveForm()
    agreement_proposal_form = LandAgreementProposalForm()
    final_approval_form = LandFinalApprovalForm()
    # land_request_final_approval_btn
    
    active_request_owner = LandRepository.get_land_parcel_request_as_owner(parcel_req_id)
    contact_details = LandRepository.get_land_application_contact_details(parcel_req_id)
    parcel_req_stages = LandRepository.get_land_request_stages(parcel_req_id)
    site_inspection_data = LandRepository.get_site_inspection_details(parcel_req_id)
    verification_docs = LandRepository.get_document_verification_files(parcel_req_id)
    all_verified = bool(verification_docs) and all(doc['verified_by'] is not None for doc in verification_docs)
    
    land_parcel_categories = LandRepository.get_land_categories()
    if land_parcel_categories:
        category_choices = [(int(cat['category_id']), cat['name']) for cat in land_parcel_categories]
    else:
        category_choices = []
        
    agreement_proposal_form.land_agreement_intended_use.choices = [('', 'Please Select Intended Use')] + category_choices
    proposal_data = LandRepository.get_agreement_proposal_details(parcel_req_id)
    
    return render_template('land/view_land_application_owner.html',
                           application_stage_form=application_stage_form,
                           inspection_stage_form=inspection_stage_form,
                           inspection_confirm_form=inspection_confirm_form,
                           doc_verification_form=doc_verification_form,
                           agreement_proposal_form=agreement_proposal_form,
                           final_approval_form=final_approval_form,
                           active_request_owner=active_request_owner,
                           contact_details=contact_details,
                           parcel_req_stages=parcel_req_stages,
                           site_inspection_data=site_inspection_data,
                           verification_docs=verification_docs,
                           all_verified=all_verified,
                           proposal_data=proposal_data)    
    
@land.route('/land/request/incoming/<int:parcel_req_id>/accept', methods=['GET', 'POST'])
@auth_required
def approve_application_stage_as_owner(parcel_req_id):
    
    try:
        
        application_stage_form = LandApplicationStageForm()
        if application_stage_form.validate_on_submit():
            
            result = LandRepository.application_stage_approval_as_owner(parcel_req_id)
        
            if not result:
                flash('Something went wrong', 'warning')
            else:
                flash('Application stage approved', 'success')
    except Exception as e:
        flash('An error occurred while Approving request.', 'danger')
    
    # Redirect back to the referring URL
    redirect_url = request.referrer or url_for('land.view_land_request_as_owner')
    return redirect(redirect_url)

    
@land.route('/land/request/incoming/<int:parcel_req_id>/decline', methods=['GET', 'POST'])
@auth_required
def decline_application_stage_as_owner(parcel_req_id):
    
    try:
        application_stage_form = LandApplicationStageForm()
        
        if application_stage_form.validate_on_submit():
            
            result = LandRepository.application_stage_rejection_as_owner(parcel_req_id)
        
            if not result:
                flash('Something went wrong', 'warning')
            else:
                flash('Application Declined', 'success')
    except Exception as e:
        flash('An error occurred while Approving request.', 'danger')
    
    # Redirect back to the referring URL
    redirect_url = request.referrer or url_for('land.view_land_request_as_owner')
    return redirect(redirect_url)
    

@land.route('/land/request/incoming/<int:parcel_req_id>/inspection', methods=['GET', 'POST'])
@auth_required
def sent_site_inspection_invite_as_owner(parcel_req_id):
    
    try:
        
        inspection_data = {}
        inspection_stage_form = LandInspectionInviteForm()
        if inspection_stage_form.validate_on_submit():
            
            inspection_data.update({
                'inspection_date' : inspection_stage_form.land_inspection_date.data,
                'inspection_start_time' : inspection_stage_form.land_inspection_start_time.data,
                'inspection_end_time' : inspection_stage_form.land_inspection_end_time.data,
                'application_id' : parcel_req_id,
                'created_by' : session['user_id']
            })
            
            
            result = LandRepository.add_site_inspection_details(inspection_data)
        
            if not result:
                flash('Something went wrong', 'warning')
            else:
                flash('Site inspection invite sent successfully', 'success')
    except Exception as e:
        flash('An error occurred while senting the request.', 'danger')
    
    # Redirect back to the referring URL
    redirect_url = request.referrer or url_for('land.view_land_request_as_owner')
    return redirect(redirect_url)


@land.route('/land/request/incoming/<int:parcel_req_id>/inspection/accept', methods=['GET', 'POST'])
@auth_required
def approve_or_decline_inspection_stage_as_owner(parcel_req_id):
    
    try:
        
        insp_data = {}
        inspection_confirm_form = LandInspectionConfirmationForm()
        
        if inspection_confirm_form.validate_on_submit():
            
            insp_data.update({
                'inspection_note': inspection_confirm_form.land_inspection_note.data,
                'land_request_id' : parcel_req_id
            })
            
            if inspection_confirm_form.land_inspection_approval_btn.data:
                
                result = LandRepository.inspection_stage_approval_as_owner(insp_data)
        
                if not result:
                    flash('Something went wrong', 'warning')
                else:
                    flash('Site Inspection stage approved', 'success')
            
            if inspection_confirm_form.land_inspection_decline_btn.data:
                result = LandRepository.inspection_stage_declined_as_owner(insp_data)
        
                if not result:
                    flash('Something went wrong', 'warning')
                else:
                    flash('Site Inspection stage Declined', 'success')
                    
    except Exception as e:
        flash('An error occurred while Approving request.', 'danger')
    
    # Redirect back to the referring URL
    redirect_url = request.referrer or url_for('land.view_land_request_as_owner')
    return redirect(redirect_url)


@land.route('/land/request/incoming/<int:parcel_req_id>/doc/verification/accept', methods=['GET', 'POST'])
@auth_required
def approve_document_verification_stage_as_owner(parcel_req_id):
    
    try:
        
        document_verification_form = LandDocVerificationApproveForm()
        
        if document_verification_form.validate_on_submit():
            
            result = LandRepository.document_verification_approval_as_owner(parcel_req_id)
        
            if not result:
                flash('Something went wrong', 'warning')
            else:
                flash('Documents Verified', 'success')
    except Exception as e:
        flash('An error occurred while Approving request.', 'danger')
    
    # Redirect back to the referring URL
    redirect_url = request.referrer or url_for('land.view_land_request_as_owner')
    return redirect(redirect_url)


@land.route('/land/request/incoming/<int:parcel_req_id>/agreement', methods=['GET', 'POST'])
@auth_required
def submit_agreement_proposal_as_owner(parcel_req_id):
    
    try:
        
        agreement_proposal_form = LandAgreementProposalForm()        
        proposal_data = {}
        
        if agreement_proposal_form.validate_on_submit():
            
            proposal_data.update({
                'application_id' : parcel_req_id,
                'tenant_id' : None,
                'lease_from' : agreement_proposal_form.land_agreement_lease_from_date.data,
                'lease_to' : agreement_proposal_form.land_agreement_lease_to_date.data,
                'rent' : agreement_proposal_form.land_agreement_rent.data,
                'pricing_modal' : agreement_proposal_form.land_agreement_modal.data,
                'intended_use' : agreement_proposal_form.land_agreement_intended_use.data,
                'security_deposit' : agreement_proposal_form.land_agreement_security.data,
                'notes' : agreement_proposal_form.land_agreement_notes.data
            })
            
            proposal_agreement_doc = agreement_proposal_form and agreement_proposal_form.land_agreement_proposal_doc.data

            if proposal_agreement_doc:
            
                # Save the file
                ext = os.path.splitext(proposal_agreement_doc.filename)[1]
                newname = f"{session['user_id']}proposal{int(time.time())}{ext}"

                upload_folder = os.path.join(current_app.static_folder, current_app.config['UPLOAD_FOLDER_LAND'], 'docs/proposal')
                result = Utils.upload_file(proposal_agreement_doc, upload_folder, newname)

                if result:
                    print("Proposal doc uploaded")
                else:
                    print("Proposal doc uploading failed")

                identity_doc_path=f"{current_app.config['UPLOAD_FOLDER_LAND']}/docs/{newname}"

                proposal_data.update({
                    'proposal_doc': identity_doc_path
                })
            
            result = LandRepository.sent_agreement_proposal_as_owner(proposal_data)
        
            if not result:
                flash('Something went wrong', 'warning')
            else:
                flash(' Agreement proposal document has been sent to the tenant. ', 'success')
    except Exception as e:
        flash('An error occurred while Approving request.', 'danger')
    
    # Redirect back to the referring URL
    redirect_url = request.referrer or url_for('land.view_land_request_as_owner')
    return redirect(redirect_url)



@land.route('/land/request/incoming/<int:parcel_req_id>/lease/accept', methods=['GET', 'POST'])
@auth_required
def start_land_lease_as_owner(parcel_req_id):
    
    try:
        
        start_lease_form = LandFinalApprovalForm()        
        lease_data = {}
        
        if start_lease_form.validate_on_submit():
            
            parcel_data = LandRepository.get_land_parcel_request_as_owner(parcel_req_id)
            
            lease_data.update({
                'application_id' : parcel_req_id,
                'land_parcel_id' : parcel_data[0]['land_parcel_id']
            })
            
            result = LandRepository.initiate_lease_as_owner(lease_data)
        
            if not result:
                flash('Something went wrong', 'warning')
            else:
                flash('Land Lease Initiated Successfully ', 'success')
    except Exception as e:
        flash('An error occurred while Approving request.', 'danger')
    
    # Redirect back to the referring URL
    redirect_url = request.referrer or url_for('land.view_land_request_as_owner')
    return redirect(redirect_url)


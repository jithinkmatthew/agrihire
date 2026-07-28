import os
import time
from flask import Blueprint, current_app, flash, redirect, render_template, request, session, url_for
from app.Utils import Utils
from app.controllers.auth.auth_controller import auth_required
from app.controllers.equipment.equipment_form import DeleteEquipmentForm, EquipmentForm, ManageEquipmentRequestForm, PublishEquipmentForm, UnPublishEquipmentForm
from app.controllers.order.order_form import OrderForm
from app.controllers.weather.weather_form import WeatherForecast
from app.model.equipment import EquipmentRepository
from app.model.user import UserRepository


equipment = Blueprint('equipment', __name__)
        
class EquipmentObjWrapper:
    def __init__(self, equip_data, safety_data=None, equip_files=None):
        self.equipment_name = equip_data.get('name')
        self.equipment_make = equip_data.get('make')
        self.equipment_model = equip_data.get('model')
        self.equipment_year = str(equip_data.get('year')) if equip_data.get('year') is not None else None
        self.equipment_category = equip_data.get('category_name')
        self.equipment_sub_category_parent_id = equip_data.get('sub_category_parent_id')
        self.equipment_sub_category = equip_data.get('sub_category_name')
        self.equipment_sub_category_id = equip_data.get('sub_category_id')
        self.equipment_description = equip_data.get('description')
        self.equipment_price = str(equip_data.get('price')) if equip_data.get('price') is not None else None
        self.equipment_price_modal = equip_data.get('price_modal')
        self.location_region = equip_data.get('region')
        self.location_district_region_id = equip_data.get('district_region_id')
        self.location_district = equip_data.get('district')
        self.location_suburb_district_id = equip_data.get('suburb_district_id')
        self.location_suburbs = equip_data.get('suburb')
        self.location_street_name = equip_data.get('street_name')
        self.location_city = equip_data.get('city')
        self.location_zip = equip_data.get('zip')
        self.location_gps_coordinate = f"{equip_data.get('latitude')}, {equip_data.get('longitude')}"
        self.equipment_height = str(equip_data.get('height')) if equip_data.get('height') is not None else None
        self.equipment_length = str(equip_data.get('length')) if equip_data.get('length') is not None else None
        self.equipment_width = str(equip_data.get('width')) if equip_data.get('width') is not None else None
        self.equipment_weight = str(equip_data.get('weight')) if equip_data.get('weight') is not None else None
        # self.safety_equipments = []  
        
        if safety_data:
            self.safety_equipments = [str(item['safety_id']) for item in safety_data]
        else:
            self.safety_equipments = []
            
        if equip_files:
            safety_docs = [item['file_path'] for item in equip_files if item['file_type'] == 'safety_doc']
            self.safety_docs = safety_docs
        else:
            self.safety_docs = None
            
        if equip_files:
            equipment_image = [item['file_path'] for item in equip_files if item['file_type'] == 'image']
            self.equipment_image = equipment_image
        else:
            self.equipment_image = None


@equipment.route('/equipment/categories', methods=['GET'])
def equipment_categories():
    
    categories = EquipmentRepository.get_equipment_categories();
    
    return categories
    
@equipment.route('/equipment/subcategories/<int:category_id>', methods=['GET'])
def equipment_subcategories(category_id):
    
    sub_categories = EquipmentRepository.get_equipment_subcategories(category_id=category_id)
    
    return sub_categories;


@equipment.route('/equipments/manage/add', methods=['GET', 'POST'])
@auth_required
def add_new_equipment():
    
    # user_name = session['username']
    # user = UserRepository.get_user(username=user_name)
    
    form = EquipmentForm()
    
    categories = EquipmentRepository.get_equipment_categories()
    category_choices = [(int(cat['category_id']), cat['name']) for cat in categories]
    form.equipment_category.choices = category_choices
    
    sub_categories = EquipmentRepository.get_all_equipment_categories()
    sub_category_choices = [(int(sub['subcategory_id']), sub['name']) for sub in sub_categories]
    form.equipment_sub_category.choices = sub_category_choices
    
    safety_options = EquipmentRepository.get_safety_options()
    formated_safety_options = [(int(item['safety_id']), item['name']) for item in safety_options]
    form.safety_equipments.choices = formated_safety_options
    
    if form.validate_on_submit():
    
        equipment_data = {
            'equipment_name' : form.equipment_name.data,
            'equipment_make' : form.equipment_make.data,
            'equipment_model' : form.equipment_model.data,
            'equipment_year' : form.equipment_year.data,
            'equipment_category' : form.equipment_category.data,
            'equipment_sub_category' : form.equipment_sub_category.data,
            'user_id' : session['user_id'],
            'equipment_description' : form.equipment_description.data,
            'equipment_price' : form.equipment_price.data,
            'equipment_price_modal' : form.equipment_price_modal.data,
            'location_region' : form.location_region.data,
            'location_district' : form.location_district.data,
            'location_suburbs' : form.location_suburbs.data,
            'location_street_name' : form.location_street_name.data,
            'location_city' : form.location_city.data,
            'location_zip' : form.location_zip.data,
            'location_gps_coordinate' : form.location_gps_coordinate.data,
            'equipment_height' : form.equipment_height.data,
            'equipment_length' : form.equipment_length.data,
            'equipment_width' : form.equipment_width.data,
            'equipment_weight' : form.equipment_weight.data,
            'safety_equipments' : form.safety_equipments.data,
            'safety_docs' : form.safety_docs.data,
            'equipment_image' : form.equipment_image.data
        }
        
        safety_docs = equipment_data.get('safety_docs', [])
        equipment_name = equipment_data['equipment_name']
        equipment_image = equipment_data.get('equipment_image', [])
        result = ''
        equipment_files = {}
        
        if safety_docs and safety_docs.filename:
            
            # Save the file
            ext = os.path.splitext(safety_docs.filename)[1]
            # newname = f"{user['user_id']}safetydoc{equipment_name.lower().replace(' ', '')}{ext}"
            # newname = f"{user['user_id']}safetydoc{ext}"
            # newname = Utils.unique_time_filename(user['user_id'], )
            newname = f"{session['user_id']}doc{int(time.time())}{ext}"
            
            upload_folder = os.path.join(current_app.static_folder, current_app.config['UPLOAD_FOLDER_EQUIPMENT'], 'docs')
            result = Utils.upload_file(safety_docs, upload_folder, newname)
            
            if result:
                print("Safety doc uploaded")
            else:
                print("Safety doc uploading failed")
            
            safety_doc_path=f"{current_app.config['UPLOAD_FOLDER_EQUIPMENT']}/docs/{newname}"
            
            equipment_files.update({
                'safety_docs': [safety_doc_path]
            })
        
        if equipment_image and equipment_image.filename:
            
            # Save the file
            ext = os.path.splitext(equipment_image.filename)[1]
            # newname = f"{user['user_id']}equipimage{ext}"
            newname = f"{session['user_id']}image{int(time.time())}{ext}"
            upload_folder = os.path.join(current_app.static_folder, current_app.config['UPLOAD_FOLDER_EQUIPMENT'], 'images')
            result = Utils.upload_file(equipment_image, upload_folder, newname)
            
            if result:
                print("Equipment image uploaded")
            else:
                print("Equipment image uploading failed")
            
            equipment_image_path=f"{current_app.config['UPLOAD_FOLDER_EQUIPMENT']}/images/{newname}"
            
            equipment_files.update({
                'equipment_image': [equipment_image_path]
            })
        
        result = EquipmentRepository.add_equipment(equipment_data, equipment_files, session['user_id'])
    
        if result > 0:
            flash('🚀 Ready to go! Give it a quick check and publish to go live.', 'success')
        
        return redirect(url_for('equipment.manage_equipments'))
        
    return render_template('equipment/manage_equipment_listing.html', form=form)    
    
@equipment.route('/equipments/manage', methods=['GET'])
@auth_required
def manage_equipments():
    
    # user_name = session['username']
    # user = UserRepository.get_user(username=user_name)
    
    form = EquipmentForm()
    delete_form = DeleteEquipmentForm()
    publish_form = PublishEquipmentForm()
    unpublish_form = UnPublishEquipmentForm()
    
    safety_options = EquipmentRepository.get_safety_options()
    formated_safety_options = [(int(item['safety_id']), item['name']) for item in safety_options]
    form.safety_equipments.choices = formated_safety_options
    
    # Populate the choices for the pricing_model field
    form.equipment_price_modal.choices = [
        ('per_hour', 'Per Hour'),
        ('per_day', 'Per Day')
    ]
    
    equipments = EquipmentRepository.get_equipments(session['user_id'])
    equipment_ids = [eq['equipment_id'] for eq in equipments]
    equipments_files = EquipmentRepository.get_equipment_files(equipment_ids)
    safety_options_for_display = EquipmentRepository.get_equipments_safety_options()
    active_rentals_as_owner = EquipmentRepository.get_active_rentals_as_owner(session['user_id'])
    
    equipment_forms = {}
    
    edit_form = None
    eq_id = None
        
    for eq in equipments:
        
        equip_safety_options = EquipmentRepository.get_equipment_safety_options(eq["equipment_id"])
        eq_id = eq['equipment_id']
        equipment_files = EquipmentRepository.get_equipment_files([eq_id])
        equipment_obj = EquipmentObjWrapper(eq, equip_safety_options, equipment_files)
        edit_form = EquipmentForm(obj=equipment_obj)
        
        categories = EquipmentRepository.get_equipment_categories()
        category_choices = [(int(cat['category_id']), cat['name']) for cat in categories]
        edit_form.equipment_category.choices = category_choices
        edit_form.equipment_category.data = equipment_obj.equipment_sub_category_parent_id
        
        sub_categories = EquipmentRepository.get_equipment_subcategories(equipment_obj.equipment_sub_category_parent_id)
        sub_category_choices = [(int(sub['subcategory_id']), sub['name']) for sub in sub_categories]
        edit_form.equipment_sub_category.choices = sub_category_choices
        edit_form.equipment_sub_category.data = equipment_obj.equipment_sub_category_id

        edit_form.equipment_price_modal.choices = [
            ('per_hour', 'Per Hour'),
            ('per_day', 'Per Day')
        ]
        regions = EquipmentRepository.get_regions();
        region_choices = [(reg['region_id'], reg['name']) for reg in regions]
        edit_form.location_region.choices = region_choices
        edit_form.location_region.data = equipment_obj.location_region
        
        districts = EquipmentRepository.get_districts(equipment_obj.location_district_region_id)
        district_choices = [(dist['district_id'], dist['name']) for dist in districts]
        edit_form.location_district.choices = district_choices
        edit_form.location_district.data = equipment_obj.location_district
        
        suburbs = EquipmentRepository.get_suburbs(equipment_obj.location_suburb_district_id)
        suburb_choices = [(sub['suburb_id'], sub['name']) for sub in suburbs]
        edit_form.location_suburbs.choices = suburb_choices
        edit_form.location_suburbs.data = equipment_obj.location_suburbs
        
        safety_options = EquipmentRepository.get_safety_options()
        edit_form.safety_equipments.choices = [(int(item['safety_id']), item['name']) for item in safety_options]
        edit_form.safety_docs.data = [item['file_path'] for item in equipment_files if item['file_type'] == 'safety_doc']
        edit_form.equipment_image.data = [item['file_path'] for item in equipment_files if item['file_type'] == 'image']
        
        equipment_forms[eq['equipment_id']] = edit_form
        
            
    return render_template('equipment/manage_equipment_listing.html', 
                           form=form,
                        #    edit_form=edit_form,
                           delete_form=delete_form,
                           publish_form=publish_form,
                           unpublish_form=unpublish_form,
                           equipment_forms=equipment_forms,
                           equipments=equipments, 
                           equipments_files=equipments_files, 
                           safety_options_for_display=safety_options_for_display,
                           active_rentals_as_owner=active_rentals_as_owner)

@equipment.route('/equipments/manage/<int:equipment_id>/edit', methods=['GET', 'POST'])
@auth_required
def edit_equipment(equipment_id):
    
    original_equipment = EquipmentRepository.get_equipment(equipment_id)
    equip_safety_options = EquipmentRepository.get_equipment_safety_options(equipment_id)
    equipment_files = EquipmentRepository.get_equipment_files([equipment_id])
    equipment_obj = EquipmentObjWrapper(original_equipment[0], equip_safety_options, equipment_files)
    
    categories = EquipmentRepository.get_equipment_categories()
    category_choices = [(int(cat['category_id']), cat['name']) for cat in categories]

    sub_categories = EquipmentRepository.get_equipment_subcategories(equipment_obj.equipment_sub_category_parent_id)
    sub_category_choices = [(int(sub['subcategory_id']), sub['name']) for sub in sub_categories]

    regions = EquipmentRepository.get_regions()
    region_choices = [(int(reg['region_id']), reg['name']) for reg in regions]

    districts = EquipmentRepository.get_districts(equipment_obj.location_district_region_id)
    district_choices = [(int(dist['district_id']), dist['name']) for dist in districts]

    suburbs = EquipmentRepository.get_suburbs(equipment_obj.location_suburb_district_id)
    suburb_choices = [(int(sub['suburb_id']), sub['name']) for sub in suburbs]

    safety_options = EquipmentRepository.get_safety_options()
    safety_choices = [(int(item['safety_id']), item['name']) for item in safety_options]

    # Instantiate form, passing POST data only if it is a POST request, else pass obj for pre-filled form
    if request.method == 'POST':
        edit_form = EquipmentForm(request.form)
    else:
        edit_form = EquipmentForm(obj=equipment_obj)

    # Assign choices before validation or rendering
    edit_form.equipment_category.choices = category_choices
    edit_form.equipment_sub_category.choices = sub_category_choices
    edit_form.equipment_price_modal.choices = [
        ('per_hour', 'Per Hour'),
        ('per_day', 'Per Day')
    ]
    edit_form.location_region.choices = region_choices
    edit_form.location_district.choices = district_choices
    edit_form.location_suburbs.choices = suburb_choices
    edit_form.safety_equipments.choices = safety_choices
    
    edit_form.safety_docs.data = [ item['file_path'] for item in equipment_files if item['file_type'] == 'safety_doc' ]
    edit_form.equipment_image.data = [item['file_path'] for item in equipment_files if item['file_type'] == 'image']

    # For GET, set select field current values from equipment_obj
    if request.method == 'GET':
        edit_form.equipment_category.data = equipment_obj.equipment_sub_category_parent_id
        edit_form.equipment_sub_category.data = equipment_obj.equipment_sub_category_id
        edit_form.location_region.data = equipment_obj.location_region
        edit_form.location_district.data = equipment_obj.location_district
        edit_form.location_suburbs.data = equipment_obj.location_suburbs
        
        # edit_form.safety_docs.data = [ item['file_path'] for item in equipment_files if item['file_type'] == 'safety_doc' ]
        

    if edit_form.validate_on_submit():
        changed_data = {}

        # Compare fields, add any changed data to changed_data dict
        if edit_form.equipment_name.data != original_equipment[0]['name']:
            changed_data['equipment_name'] = edit_form.equipment_name.data

        if edit_form.equipment_make.data != original_equipment[0]['make']:
            changed_data['equipment_make'] = edit_form.equipment_make.data

        if edit_form.equipment_model.data != original_equipment[0]['model']:
            changed_data['equipment_model'] = edit_form.equipment_model.data

        if edit_form.equipment_year.data != str(original_equipment[0]['year']):
            changed_data['equipment_year'] = edit_form.equipment_year.data

        if edit_form.equipment_category.data != original_equipment[0]['sub_category_parent_id']:
            changed_data['equipment_category_id'] = edit_form.equipment_category.data

        if edit_form.equipment_sub_category.data != original_equipment[0]['sub_category_id']:
            changed_data['equipment_sub_category_id'] = edit_form.equipment_sub_category.data

        if edit_form.equipment_description.data != original_equipment[0]['description']:
            changed_data['equipment_description'] = edit_form.equipment_description.data

        if edit_form.equipment_price.data != str(original_equipment[0]['price']):
            changed_data['equipment_price'] = edit_form.equipment_price.data

        if edit_form.equipment_price_modal.data != original_equipment[0]['price_modal']:
            changed_data['equipment_price_modal'] = edit_form.equipment_price_modal.data

        if edit_form.location_region.data != original_equipment[0]['district_region_id']:
            changed_data['location_region_id'] = edit_form.location_region.data

        if edit_form.location_district.data != original_equipment[0]['suburb_district_id']:
            changed_data['location_district_id'] = edit_form.location_district.data

        if edit_form.location_suburbs.data != original_equipment[0]['suburb_id']:
            changed_data['location_suburb_id'] = edit_form.location_suburbs.data

        if edit_form.location_street_name.data != original_equipment[0]['street_name']:
            changed_data['location_street_name'] = edit_form.location_street_name.data

        if edit_form.location_city.data != original_equipment[0]['city']:
            changed_data['location_city'] = edit_form.location_city.data

        if edit_form.location_zip.data != original_equipment[0]['zip']:
            changed_data['location_zip'] = edit_form.location_zip.data

        if edit_form.location_gps_coordinate.data != f"{original_equipment[0]['latitude']}, {original_equipment[0]['longitude']}":
            changed_data['location_gps_coordinate'] = edit_form.location_gps_coordinate.data

        if edit_form.equipment_height.data != str(original_equipment[0]['height']):
            changed_data['equipment_height'] = edit_form.equipment_height.data

        if edit_form.equipment_length.data != str(original_equipment[0]['length']):
            changed_data['equipment_length'] = edit_form.equipment_length.data

        if edit_form.equipment_width.data != str(original_equipment[0]['width']):
            changed_data['equipment_width'] = edit_form.equipment_width.data

        if edit_form.equipment_weight.data != str(original_equipment[0]['weight']):
            changed_data['equipment_weight'] = edit_form.equipment_weight.data

        if set(edit_form.safety_equipments.data) != set([item['safety_id'] for item in equip_safety_options]):
            changed_data['safety_equipments'] = edit_form.safety_equipments.data

        # Safety Docs
        uploaded_doc = request.files.get('safety_docs')
        if uploaded_doc and uploaded_doc.filename:
            ext = os.path.splitext(uploaded_doc.filename)[1]
            # newname = f"{user['user_id']}safetydoc{ext}"
            newname = f"{session['user_id']}doc{int(time.time())}{ext}"
            upload_folder = os.path.join(current_app.static_folder, current_app.config['UPLOAD_FOLDER_EQUIPMENT'], 'docs')
            # remove existing file
            existing_doc_filename = next((item['file_path'] for item in equipment_files if item['file_type'] == 'safety_doc'),None)
            
            if existing_doc_filename:

                # Construct full path
                existing_doc_location = os.path.join(
                    current_app.static_folder,
                    existing_doc_filename  # assuming file_path is relative to static folder
                )
                
                if os.path.exists(existing_doc_location):
                    os.remove(existing_doc_location)
                    
            result = Utils.upload_file(uploaded_doc, upload_folder, newname)

            if result:
                changed_data['safety_docs'] = os.path.join(current_app.config['UPLOAD_FOLDER_EQUIPMENT'], 'docs', newname)        
        
        # Image File
        uploaded_image = request.files.get('equipment_image')
        if uploaded_image and uploaded_image.filename:
            # Save the file
            ext = os.path.splitext(uploaded_image.filename)[1]
            # newname = f"{user['user_id']}equipimage{ext}"
            newname = f"{session['user_id']}image{int(time.time())}{ext}"
            upload_folder = os.path.join(current_app.static_folder, current_app.config['UPLOAD_FOLDER_EQUIPMENT'], 'images')
            # remove existing file
            existing_image_filename = next((item['file_path'] for item in equipment_files if item['file_type'] == 'image'),None)
            
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
                changed_data['equipment_image'] = os.path.join(current_app.config['UPLOAD_FOLDER_EQUIPMENT'], 'images', newname)
        
        
        if changed_data:
            result = EquipmentRepository.edit_equipment(changed_data, equipment_id)
            
            if result > 0:
                flash('Changes saved! Please publish to the public.', 'success')
            return redirect(url_for('equipment.manage_equipments'))
        else:
            
            flash("No changes were made.", "danger")

    # Render the edit equipment page with the form and equipment object
    return redirect(url_for('equipment.manage_equipments'))

@equipment.route('/equipment/<int:equip_id>', methods=['GET'])
@auth_required
def view_equipment(equip_id):
    try:
        equipment = EquipmentRepository.get_equipment(equip_id)
        eq_id = [equip_id]
        equipment_files = EquipmentRepository.get_equipment_files(eq_id)
        safety_options_for_display = EquipmentRepository.get_equipment_safety_options(equip_id)
        
        
        order_form=OrderForm()
        weather_forecast_form=WeatherForecast()
        
        # the data
        
    except Exception as e:
        flash('An error occurred while viewing equipment.', 'danger')
    
    return render_template('equipment/view_equipment.html', 
                           equipment=equipment,
                           equipment_files=equipment_files,
                           safety_options_for_display=safety_options_for_display,
                           order_form=order_form,
                           weather_forecast_form=weather_forecast_form)


@equipment.route('/equipment/manage/<int:equip_id>/delete', methods=['POST'])
@auth_required
def delete_equipment(equip_id):
    try:
        
        result = EquipmentRepository.delete_equipment(equip_id)
        if not result:
            flash('Equipment not found or could not be deleted.', 'warning')
        else:
            flash('Equipment deleted successfully.', 'success')
    except Exception as e:
        flash('An error occurred while deleting equipment.', 'danger')
    
    # Redirect back to the referring URL
    redirect_url = request.referrer or url_for('equipment.manage_equipments')
    return redirect(redirect_url)

@equipment.route('/equipment/manage/<int:equip_id>/publish', methods=['POST'])
@auth_required
def publish_equipment(equip_id):
    try:
        
        result = EquipmentRepository.publish_equipment(equip_id)
        if not result:
            flash('Equipment could not be published.', 'warning')
        else:
            flash('Equipment published successfully.', 'success')
    except Exception as e:
        flash('An error occurred while publishing equipment.', 'danger')
    
    # Redirect back to the referring URL
    redirect_url = request.referrer or url_for('equipment.manage_equipments')
    return redirect(redirect_url)

@equipment.route('/equipment/manage/<int:equip_id>/unpublish', methods=['POST'])
@auth_required
def unpublish_equipment(equip_id):
    try:
        
        result = EquipmentRepository.unpublish_equipment(equip_id)
        if not result:
            flash('Equipment could not be Unpublished.', 'warning')
        else:
            flash('Equipment Unpublished successfully.', 'success')
    except Exception as e:
        flash('An error occurred while Unpublishing equipment.', 'danger')
    
    # Redirect back to the referring URL
    redirect_url = request.referrer or url_for('equipment.manage_equipments')
    return redirect(redirect_url)
    
# @equipment.route('/equipment/manage', methods=['GET', 'POST'])
# @auth_required
# def manage_equipment():
    
#     print("Manage eqp listing")
    
#     return render_template('equipment/manage_equipment_listing.html')


@equipment.route('/equipment/request/outgoing', methods=['GET'])
@auth_required
def view_equipment_request_as_renter():
    
    user_id = session.get('user_id')
    active_rentals_as_renter = EquipmentRepository.get_active_rentals_as_renter(user_id)
    ids = [e['equipment_id'] for e in active_rentals_as_renter]
    active_equipment_files = EquipmentRepository.get_equipment_files(ids)
    
    past_rentals_as_renter = EquipmentRepository.get_past_rentals_as_renter(user_id)
    ids = [e['equipment_id'] for e in past_rentals_as_renter]
    past_equipment_files = EquipmentRepository.get_equipment_files(ids)
    
    return render_template('equipment/my_equipment_request.html',
                           active_rentals_as_renter=active_rentals_as_renter,
                           active_equipment_files=active_equipment_files,
                           past_rentals_as_renter=past_rentals_as_renter,
                           past_equipment_files=past_equipment_files)
    
@equipment.route('/equipment/request/incoming', methods=['GET', 'POST'])
@auth_required
def view_equipment_request_as_owner():
    
    manage_request_form = ManageEquipmentRequestForm()
    user_id = session.get('user_id')
    
    active_rentals_as_owner = EquipmentRepository.get_active_rentals_as_owner(user_id)
    ids = [e['equipment_id'] for e in active_rentals_as_owner]
    active_equipment_files = EquipmentRepository.get_equipment_files(ids)
    
    past_rentals_as_owner = EquipmentRepository.get_past_rentals_as_owner(user_id)
    ids = [e['equipment_id'] for e in past_rentals_as_owner]
    past_equipment_files = EquipmentRepository.get_equipment_files(ids)
    
    return render_template('equipment/incoming_equipment_request.html',
                           manage_request_form=manage_request_form,
                           active_rentals_as_owner=active_rentals_as_owner,
                           active_equipment_files=active_equipment_files,
                           past_rentals_as_owner=past_rentals_as_owner,
                           past_equipment_files=past_equipment_files)


@equipment.route('/equipment/request/update/<int:equip_req_id>', methods=['POST'])
@auth_required
def update_equipment_request_as_owner(equip_req_id):
    
    manage_request_form = ManageEquipmentRequestForm()
    
    if manage_request_form.validate_on_submit():
        print("hello")

        status = manage_request_form.equipment_status.data
        equip_req = EquipmentRepository.get_equipment_request(equip_req_id)
        equip_id = equip_req[0].get('equipment_id')
        
        # Change the status back to listed(publish) once the process complete
        if (status == 'listed'):
            
            result = (EquipmentRepository.update_hired_status(0, equip_id) and
                        EquipmentRepository.update_equipment_status(status, equip_id) and
                        EquipmentRepository.update_equipment_request_status(0, equip_req_id))

            if result:
                pass
        else:
               
            result = EquipmentRepository.update_equipment_status(status, equip_id)
            if result:
                pass
        
        return redirect(url_for('equipment.view_equipment_request_as_owner'))
    
    return redirect(url_for('equipment.view_equipment_request_as_owner'))

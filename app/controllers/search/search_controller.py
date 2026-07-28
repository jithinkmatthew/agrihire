import os
import time
from flask import Blueprint, current_app, flash, jsonify, redirect, render_template, request, session, url_for
from app.Utils import Utils
# from app.controllers.search.search_form import SearchForm
from app.controllers.auth.auth_controller import auth_required
from app.controllers.search.search_form import EquipmentSearchForm, LandSearchForm
from app.model.equipment import EquipmentRepository
from app.model.land import LandRepository
from app.model.location import LocationRepository
from app.model.search import SearchRepository
from app.model.user import UserRepository

search = Blueprint('search', __name__)

@search.route('/search', methods=['GET', 'POST'])
def search_assets():
    
    if request.args.get('new_search') == '1':
        session.pop('last_equipment_search', None)
        session.pop('last_land_search', None)
    
    equipment_results = None
    land_results = None
    
    equipment_searched = False
    land_searched = False
    
    equipment_form = EquipmentSearchForm(prefix='equip', data=session.get('last_equipment_search'))
    land_form = LandSearchForm(prefix='land', data=session.get('last_land_search'))
    
    # Equipment Categories
    equip_categories = EquipmentRepository.get_equipment_categories()
    equip_category_choices = [(int(cat['category_id']), cat['name']) for cat in equip_categories]
    equipment_form.equipment_category.choices = [(0, 'All Categories')] + equip_category_choices
    
    # Land Categories
    land_categories = LandRepository.get_land_categories()
    land_category_choices = [(int(cat['category_id']), cat['name']) for cat in land_categories]
    land_form.land_category.choices = [(0, 'All Categories')] + land_category_choices
    
    regions = LocationRepository.get_regions()
    equip_region_choices = [(int(reg['region_id']), reg['name']) for reg in regions]
    land_region_choices = [(int(reg['region_id']), reg['name']) for reg in regions]
    equipment_form.equipment_region.choices = [(0, 'All Regions')] + equip_region_choices
    land_form.land_region.choices = [(0, 'All Regions')] + land_region_choices
    
    equip_region_id = session.get('last_equipment_search', {}).get('region_id') or equipment_form.equipment_region.data
    equip_districts = LocationRepository.get_districts(equip_region_id)
    equip_district_choices = [(int(dis['district_id']), dis['name']) for dis in equip_districts]
    equipment_form.equipment_district.choices = [(0, 'All Districts')] + equip_district_choices
    
    land_region_id = session.get('last_land_search', {}).get('region_id') or land_form.land_region.data
    land_districts = LocationRepository.get_districts(land_region_id)
    land_district_choices = [(int(dis['district_id']), dis['name']) for dis in land_districts]
    land_form.land_district.choices = [(0, 'All Districts')] + land_district_choices

    equip_district_id = session.get('last_equipment_search', {}).get('district_id') or equipment_form.equipment_district.data
    equip_suburbs = LocationRepository.get_suburbs(equip_district_id)
    equip_suburbs_choices = [(int(sub['suburb_id']), sub['name']) for sub in equip_suburbs]
    equipment_form.equipment_suburb.choices = [(0, 'All Suburbs')] + equip_suburbs_choices
    
    land_district_id = session.get('last_land_search', {}).get('district_id') or equipment_form.equipment_district.data
    land_suburbs = LocationRepository.get_suburbs(land_district_id)
    land_suburbs_choices = [(int(sub['suburb_id']), sub['name']) for sub in land_suburbs]
    land_form.land_suburb.choices = [(0, 'All Suburbs')] + land_suburbs_choices
    
    # equipments_files = EquipmentRepository.get_equipment_files(equipment_ids)

    if equipment_form.equipment_search_btn.data and equipment_form.validate_on_submit():
        search_data = {
            'category_id': equipment_form.equipment_category.data,
            'region_id': equipment_form.equipment_region.data,
            'district_id': equipment_form.equipment_district.data,
            'suburb_id': equipment_form.equipment_suburb.data,
            'user_id_logged_in': session.get('user_id', 0)
        }
        
        session['last_equipment_search'] = search_data
        equipment_results = SearchRepository.find_equipments(search_data)
        equipment_searched = True
    
    if not equipment_searched and session.get('last_equipment_search'):
        equipment_results = SearchRepository.find_equipments(session['last_equipment_search'])
        equipment_searched = True
        
        
    if land_form.land_search_btn.data and land_form.validate_on_submit():
        search_data = {
            'category_id': land_form.land_category.data,
            'region_id': land_form.land_region.data,
            'district_id': land_form.land_district.data,
            'suburb_id': land_form.land_suburb.data,
            'user_id_logged_in': session.get('user_id', 0)
        }
        
        session['last_land_search'] = search_data
        land_results = SearchRepository.find_land_parcels(search_data)
        land_searched = True
    
    if not land_searched and session.get('last_land_search'):
        land_results = SearchRepository.find_land_parcels(session['last_land_search'])
        land_searched = True
        
    # Set the selected drop down value when coming back search page
    equip_category_id = session.get('last_equipment_search', {}).get('category_id')
    if equip_category_id:
        equipment_form.equipment_category.data = equip_category_id
    
    
    equip_region_id = session.get('last_equipment_search', {}).get('region_id')
    if equip_region_id:
        equipment_form.equipment_region.data = equip_region_id
    else:
        equipment_form.equipment_region.choices = [(0, 'All Regions')] + equip_region_choices
    
    
    land_region_id = session.get('last_land_search', {}).get('region_id')
    if land_region_id:
        land_form.land_region.data = land_region_id
    else:
        land_form.land_region.choices = [(0, 'All Regions')] + land_region_choices
    
        
    equip_district_id = session.get('last_equipment_search', {}).get('district_id')
    if equip_district_id:
        equipment_form.equipment_district.data = equip_district_id
    else:
        equipment_form.equipment_district.choices = [(0, 'All Districts')] + equip_district_choices
       
    land_district_id = session.get('last_land_search', {}).get('district_id')
    if land_district_id:
        land_form.land_district.data = land_district_id
    else:
        land_form.land_district.choices = [(0, 'All Districts')] + land_district_choices
        
    equip_suburb_id = session.get('last_equipment_search', {}).get('suburb_id')
    if equip_suburb_id:
        equipment_form.equipment_suburb.data = equip_suburb_id
    else:
        equipment_form.equipment_suburb.choices = [(0, 'All Suburbs')] + equip_suburbs_choices
        
    land_suburb_id = session.get('last_land_search', {}).get('suburb_id')
    if land_suburb_id:
        land_form.land_suburb.data = land_suburb_id
    else:
        land_form.land_suburb.choices = [(0, 'All Suburbs')] + land_suburbs_choices
                
    
    return render_template('search/search_assets.html', 
                           equipment_form=equipment_form,
                           land_form=land_form,
                           equipment_results=equipment_results,
                           land_results=land_results,
                           equipment_searched=equipment_searched,
                           land_searched=land_searched)
    

@search.route('/compare_products/<string:asset_type>', methods=['POST'])
@auth_required
def compare_products(asset_type):
    
    data = request.get_json()
    asset_ids = data.get('asset_ids', [])
    
    if asset_type == 'equipment':
        equipments = []
        for eq_id in asset_ids:
            eq = EquipmentRepository.get_equipment(eq_id)
            if eq:
                equipments.append(eq[0])
        return equipments
    
    if asset_type == 'land':
        land_parcel = []
        for land_id in asset_ids:
            land = LandRepository.get_land_parcel(land_id)
            if land:
                land_parcel.append(land[0])
        return land_parcel
            


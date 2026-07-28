from flask import Blueprint
from app.model.location import LocationRepository

location = Blueprint('location', __name__)

@location.route('/regions', methods=['GET'])
def getregions():
    
    return LocationRepository.get_regions()

@location.route('/districts/<int:region_id>', methods=['GET'])
def getdistricts(region_id):
    
    return LocationRepository.get_districts(region_id=region_id)

@location.route('/suburbs/<int:district_id>', methods=['GET'])
def getsuburb(district_id):
    
    return LocationRepository.get_suburbs(district_id=district_id)
from flask import Flask, flash, render_template
from app import connect
from app import db
from flask_bcrypt import Bcrypt
from app.config import Config
from app.Utils import TimeUtils
from app.Utils import StatusFormatUtils

# Create the Flask app
app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = 'Aotearoa_Agri_Hire'

app.config.from_object(Config)


# Initialize the database
db.init_db(app, connect.dbuser, connect.dbpass, connect.dbhost, connect.dbname)

"""Create an instance of the Bcrypt class, which we'll be using to hash user
    passwords during login and registration.
"""
flask_bcrypt = Bcrypt(app)

from app.controllers.auth.auth_controller import auth as auth_blueprint
from app.controllers.user.user_controller import user as user_blueprint
from app.controllers.equipment.equipment_controller import equipment as equipment_blueprint
from app.controllers.location.location_controller import location as location_blueprint
from app.controllers.search.search_controller import search as search_blueprint
from app.controllers.order.order_controller import order as order_blueprint
from app.controllers.weather.weather_controller import weather as weather_blueprint
from app.controllers.land.land_controller import land as land_blueprint


app.register_blueprint(auth_blueprint, url_prefix='')
app.register_blueprint(user_blueprint)
app.register_blueprint(equipment_blueprint)
app.register_blueprint(location_blueprint)
app.register_blueprint(search_blueprint)
app.register_blueprint(order_blueprint)
app.register_blueprint(weather_blueprint)
app.register_blueprint(land_blueprint)


app.add_template_filter(TimeUtils.timeformat, 'timeformat')
app.add_template_filter(TimeUtils.dateformat, 'dateformat')
app.add_template_filter(TimeUtils.date_between, 'date_between')
app.add_template_filter(StatusFormatUtils.format_status_filter, 'format_status')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
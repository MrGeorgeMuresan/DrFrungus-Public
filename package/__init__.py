from flask import Flask
from flask_assets import Environment, Bundle

#BASIC CONFIG FOR THE APP
app = Flask(__name__)
assets = Environment(app)

assets.url = app.static_url_path
app.config['SECRET_KEY'] = 'SECRET_KEY'

scss = Bundle('css/main.scss', filters='pyscss', output='css/main.css')
assets.register('scss_all', scss)

from package import routs

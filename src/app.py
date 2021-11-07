from flask import Flask
from flask_cors import CORS
from . import env
from .views import login, register, token, get, put
from .database import mongo

app = Flask(__name__)
app.config["MONGO_URI"] = env.mongo_uri
app.config["SECRET_KEY"] = env.secret_key
app.config['CORS_HEADERS'] = 'Content-Type'
mongo.init_app(app)
CORS(app)

# app.register_blueprint(token.token_bp, url_prefix='/token')
app.register_blueprint(register.register_bp, url_prefix='/register')
app.register_blueprint(login.login_bp, url_prefix='/login')
app.register_blueprint(get.get_bp, url_prefix="/get")
app.register_blueprint(put.put_bp, url_prefix="/put")
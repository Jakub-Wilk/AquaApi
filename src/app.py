from flask import Flask
from flask.helpers import url_for
from . import env
from .views import login, register, token, get
from .database import mongo

app = Flask(__name__)
app.config["MONGO_URI"] = env.mongo_uri
app.config["SECRET_KEY"] = env.secret_key
mongo.init_app(app)

app.register_blueprint(token.token_bp, url_prefix='/token')
app.register_blueprint(register.register_bp, url_prefix='/register')
app.register_blueprint(login.login_bp, url_prefix='/login')
app.register_blueprint(get.get_bp, url_prefix="/get")
from flask import Blueprint

route = Blueprint('route', __name__, url_prefix='/')

@route.route('/')
def home():
    return 'Hello'
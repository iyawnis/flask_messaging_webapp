from flask import Blueprint

api = Blueprint('api', __name__)

from . import contacts, contact, push_message

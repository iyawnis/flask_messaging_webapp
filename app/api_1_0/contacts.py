from flask import make_response,request 
from bson.json_util import dumps
from dbmanager import db_collection
from . import api
from app.model import Contact

@api.route('/contacts/',methods = ['GET'])
def get_contacts():
	""" Return all database entries for our collection"""
	result = {}
	result['data'] = db_collection().find()
	result['code'] = 200 if result['data'] else 404
	return make_response(dumps(result), result['code'],{"Content-type": "application/json"})

@api.route('/contacts/',methods = ['POST'])
def post_contact():
	""" Create a new contact document, with the provided phone number and reg_id"""
	result = {}
	phone = request.form['phone_num']
	reg_id = request.form['reg_id']
	contact = Contact(phone,reg_id)
	result['data'] = db_collection().insert(contact.__dict__)
	result['code'] = 200 if result['data'] else 404
	return make_response(dumps(result), result['code'],{"Content-type": "application/json"})

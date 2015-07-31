from flask import  make_response,request 
from bson.json_util import dumps
from dbmanager import db_collection
from . import api
from app.model import Contact
@api.route('/contact/<string:phone_num>', methods=['GET'])
def get_contact(phone_num):
    """ Return the collection document for the given phone number""" 
    result = {}

    result['data'] = db_collection().find_one({Contact.phone:phone_num})
    result['code'] = 200 if result['data'] else 404
    return make_response(dumps(result), result['code'],{"Content-type": "application/json"})

@api.route('/contact/<string:phone_num>', methods=['PUT'])
def put_contact(phone_num):
    """ Update the registration ID for the given phone number""" 
    result = {}
    result['data'] = db_collection().update({Contact.phone:phone_num},{'$set':{Contact.reg_id:request.form['reg_id']}},False)
    result['code'] = 200 if result['data'] else 404
    return make_response(dumps(result), result['code'],{"Content-type": "application/json"})

@api.route('/contact/<string:phone_num>',methods=['DELETE'])
def delete_contact(phone_num):
    """ Delete the document for the given phone number""" 
    result = {}
    result['data'] = db_collection().remove({Contact.phone:phone_num})
    result['code'] = 200 if result['data'] else 404
    return make_response(dumps(result), result['code'],{"Content-type": "application/json"})

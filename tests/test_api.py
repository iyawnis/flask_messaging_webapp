from app.api_1_0.dbmanager import db,db_collection
import unittest
from app import create_app
from flask import current_app, url_for
import json
from werkzeug.routing import BuildError
from manage import drop_db, populate_db
from app.model import Contact

class APITestCase(unittest.TestCase):

	default_values = current_app.config.get('DB_EXAMPLE_VALUES')
	default_data = [{Contact.phone: default_values[0][0], Contact.reg_id: default_values[0][1]},
		 {Contact.phone: default_values[1][0], Contact.reg_id: default_values[1][1]}]

	def setUp(self):
		self.app = create_app('testing')
		self.app_context = self.app.app_context()
		self.app_context.push()
		self.setupDB()
		self.client = self.app.test_client()

	def get_json_clear(self,response):
		response_values = json.loads(response.data.decode('utf-8'))
		if type(response_values['data']) is dict:
			response_values['data'].pop('_id')
		elif type(response_values['data']) is list:
			for result in response_values['data']:
				result.pop('_id')

		return response_values

	def get_json(self,response):
		response_values = json.loads(response.data.decode('utf-8'))
		return response_values

	def setupDB(self):
		drop_db()
		populate_db()

	def tearDown(self):
	    self.app_context.pop()
	
	def test_list_contacts_valid(self):
		response = self.client.get(url_for('api.get_contacts')	)
		expected_values = {"code": 200, "data": self.default_data}
		response_values = self.get_json_clear(response)
		self.assertTrue(expected_values == response_values)

	def test_post_contact(self):		
		response = self.client.post(url_for('api.post_contact'), 
			data=dict( reg_id='username',   phone_num='321312'))
		response_values = json.loads(response.data.decode('utf-8'))
		self.assertTrue(response_values['code'] == 200)
	
	def test_post_contact_missing_attr(self):
		response = self.client.post(url_for('api.post_contact'), 
			data=dict( reg_id='username'))
		self.assertTrue(response.status_code == 400)
		self.assertTrue(response.status_code == 400)

	def test_get_contact(self):
		response = self.client.get(url_for('api.get_contact',phone_num=self.default_values[0][0]))
		response_values = self.get_json_clear(response)
		self.assertTrue(response_values['data'] == self.default_data[0])

	def test_get_contact_no_id(self):
		with self.assertRaises(BuildError):
			self.client.get(url_for('api.get_contact'))

	def test_get_contact_not_found(self):
		response = self.client.get(url_for('api.get_contact',phone_num="not even number"))
		response_values = self.get_json_clear(response)
		self.assertTrue(response_values['code'] == 404)
	
	def test_wrong_api_key(self):
		response = self.client.get(url_for('api.get_contacts')	)
		expected_values = {"code": 200, "data": self.default_data}
		response_values = self.get_json_clear(response)
		response = self.client.post(url_for('api.push_message',sender_num=self.default_values[0][0]),data=dict(phone_nums=self.default_values[1][0],msg='helasassa'))
		self.assertTrue(response.status_code == 501)












		


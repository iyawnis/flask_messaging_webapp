from bson.json_util import dumps,loads

class Contact():
	phone = 'number'
	reg_id = 'reg_id'

	def __init__(self, num,reg_id):
		int(num)
		self.number = str(num)
		self.reg_id = str(reg_id)
		

	@staticmethod
	def from_json(json_str):
		json = loads(json_str)
		num = json['number']
		reg_id = json['reg_id']
		return Contact(num,reg_id)

	def to_json(self):
		return dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
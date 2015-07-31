from flask import make_response,request,current_app
from bson.json_util import dumps
from dbmanager import db_collection
from . import api
from gcmclient import *
from app.model import Contact

@api.route('/push/<string:sender_num>',methods = ['POST'])
def push_message(sender_num):
	""" Takes a post request, with the phone number as URL parameter, and a message 'msg'
	as form parameter"""
	phone_nums = request.form['phone_nums'] #comma seperated numbers
	number_list = [s for s in phone_nums.split(',')]
	message = request.form['msg']
	gcm_id = []
	current_app.logger.debug("Pushing message to numbers %s from %s" % (number_list,sender_num))
	for num in number_list:
		document =  db_collection().find_one({Contact.phone:num})
		gcm_id.append(document[Contact.reg_id])
	result_code = gcm_send(gcm_id, message)
	return make_response(dumps(result_code), result_code,{"Content-type": "application/json"})


def gcm_send(gcm_id,message):
	dry_run_conf = current_app.config.get('DRY_RUN_API')
	api_key = current_app.config.get('GOOGLE_API')
	gcm = GCM(api_key)
	data = {'msg': message}

	# http://developer.android.com/google/gcm/server-ref.html
	# dry_rn: This parameter, when set to true, allows developers to test a request without actually sending a message.
	# collapse_key: This parameters identifies a group of messages (e.g., with collapse_key: "Updates Available") 
	# 			  that can be collapsed, so that only the last message gets sent when delivery can be resumed. 
	# 			  This is intended to avoid sending too many of the same messages when the device comes back 
	# 			  online or becomes active (see delay_while_idle).
	multicast = JSONMessage(gcm_id, data, collapse_key='my.key', dry_run=dry_run_conf)
	try:
		res_multicast = gcm.send(multicast)
		for res in [res_multicast]:
 			for reg_id, msg_id in res.success.items():
				print "Successfully sent %s as %s" % (reg_id, msg_id)
				return 200
			if res.needs_retry():
				retry_msg = res.retry()
				print "Wait or schedule task after %s seconds" % res.delay(retry)
				return 503
			print res.not_registered
			print res.failed
			print res.canonical
		return 501

	except GCMAuthenticationError, e:
		# stop and fix your settings
		current_app.logger.error("Your Google API key is rejected")
		current_app.logger.exception(e)

	except ValueError, e:
		# probably your extra options, such as time_to_live,
		# are invalid. Read error message for more info.
		current_app.logger.error("Invalid message/option or invalid GCM response:: %s " % e.args[0])
		current_app.logger.exception(e)
	except Exception,e :
		# your network is down or maybe proxy settings
		# are broken. when problem is resolved, you can
		# retry the whole message.
		current_app.logger.error("Something wrong with requests library")
		current_app.logger.exception(e)

	return 500
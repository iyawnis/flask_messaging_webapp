from flask import Flask
from config import config


def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)

	from api_1_0 import api as api_1_0_blueprint
	app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

	if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
		from flask.ext.sslfy import SSLify
		sslify = SSLify(app)

	return app
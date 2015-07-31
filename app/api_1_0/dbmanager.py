from pymongo import MongoClient
from flask import current_app,g 

def getDbConnection():
    if not hasattr(g,'mongo'):
      try:
        ip = current_app.config.get('MONGO_DB_IP')
        port = current_app.config.get('MONGO_DB_PORT')
        g.mongo = MongoClient(ip,port)
      except:
        error_msg = 'Failed to connect to database: %s' % sys.exc_info()[0]
        current_app.logger.exception(error_msg);
        # flash(error_msg)

    if g.mongo.alive():
      return g.mongo
    return None

def db_collection():
    db_connection = getDbConnection()
    db = db_connection[current_app.config.get('MONGO_DB_NAME')]
    return db[current_app.config.get('MONGO_DB_COLLECTION_NAME')]

def db():
    db_connection = getDbConnection()
    db = db_connection[current_app.config.get('MONGO_DB_NAME')]
    return db



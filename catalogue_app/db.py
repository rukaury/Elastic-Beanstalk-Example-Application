import copy
import os
from flask import g
import mysql.connector
from catalogue_app import memo_dict
from catalogue_app.config import Config


def query_mysql(query, args=None, dict_=False):
	"""Retrieve query if memoized else execute query on connection
	stored in g.
	"""
	# Check if query already cached in memo_dict
	query_pkey = _query_pkey(query, args)
	if query_pkey in memo_dict:
		# Return a deepcopy to avoid mutating and affecting future queries
		return copy.deepcopy(memo_dict[query_pkey])
	else:
		cnx = get_db(local=Config.LOCAL_DB)
		cursor = cnx.cursor(dictionary=dict_)
		cursor.execute(query, args)
		results = cursor.fetchall()
		cursor.close()
		# Save query in memo_dict for future use
		memo_dict[query_pkey] = results
		return results


def _query_pkey(query, args):
	"""Append 'query' and 'args' into a string for use as a primary key
	to represent the query. No risk of SQL injection as memo_dict will
	simply store memo_dict['malicious_query'] = None.
	"""
	return query + '.' + str(args)


def get_db(local):
	"""Connect to db and store connection in g for
	life of request.
	"""
	if 'db' not in g:
		if local:
			g.db = mysql.connector.connect(host='localhost',
										   user='admin',
										   password=os.environ.get('DB_PASSWORD'),
										   database=os.environ.get('DB_DATABASE_NAME'))
		else:
			g.db = mysql.connector.connect(host=os.environ.get('DB_HOST'),
										   user=os.environ.get('DB_USER'),
										   password=os.environ.get('DB_PASSWORD'),
										   database=os.environ.get('DB_DATABASE_NAME'))
	return g.db


def close_db(e=None):
	"""Remove connection to db from g and close."""
	db = g.pop('db', None)
	if db is not None:
		db.close()


def init_app(app):
	"""In factory function, register the close_db function so
	that connections closed at end of request.
	"""
	app.teardown_appcontext(close_db)

import os

class Config:
	DEBUG = False
	LOCAL_DB = False
	LAST_YEAR = '2018-19'
	THIS_YEAR = '2019-20'
	BABEL_DEFAULT_LOCALE = 'en'
	# Ensure FR properly displayed when returning JSON
	JSON_AS_ASCII = False
	# Load strings from environ vars to avoid storing in plaintext
	BASIC_AUTH_USERNAME = os.environ.get('BASIC_AUTH_USERNAME')
	BASIC_AUTH_PASSWORD = os.environ.get('BASIC_AUTH_PASSWORD')
	SECRET_KEY = os.environ.get('SECRET_KEY')
	GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')

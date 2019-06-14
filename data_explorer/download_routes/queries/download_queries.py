import csv
from io import StringIO
from flask_babel import gettext
from data_explorer.db import query_mysql


def general_tab(course_code):
	"""Query raw data used for the General tab."""
	query = """
		SELECT *
		FROM product_info
		WHERE course_code = %s;
	"""
	# Run query
	results = query_mysql(query, (course_code,), dict_=True)
	results_processed = _dicts_to_lists(results)
	# Create file
	file = _create_file(results_processed)
	return file


def dashboard_tab(course_code):
	"""Query raw data used for the Dashboard and Maps tabs."""
	table_name = 'lsr_this_year'
	# Exclude course_title_en and course_title_fr
	# Saves a LOT of time, space for huge courses
	query = """
		SELECT course_code, business_type, offering_id, month_en,
			   month_fr, client, offering_status, offering_language,
			   offering_region_en, offering_region_fr, offering_province_en,
			   offering_province_fr, offering_city, offering_lat,
			   offering_lng, learner_province, learner_city, learner_lat,
			   learner_lng, reg_id, reg_status, no_show, learner_id,
			   learner_language, learner_classif, billing_dept_name_en,
			   billing_dept_name_fr
		FROM {0}
		WHERE course_code = %s;
	""".format(table_name)
	# Run query
	results = query_mysql(query, (course_code,), dict_=True)
	results_processed = _dicts_to_lists(results)
	# Create file
	file = _create_file(results_processed)
	return file


# def ratings_tab(course_code):
# 	"""Query raw data used for the Ratings tab."""
# 	query = """
# 		SELECT *
# 		FROM ratings
# 		WHERE course_code = %s;
# 	"""
# 	# Run query
# 	results = query_mysql(query, (course_code,), dict_=True)
# 	results_processed = _dicts_to_lists(results)
# 	# Create file
# 	file = _create_file(results_processed)
# 	return file


def comments_tab(course_code):
	"""Query raw data used for the Comments tab."""
	query = """
		SELECT *
		FROM comments
		WHERE course_code = %s;
	"""
	# Run query
	results = query_mysql(query, (course_code,), dict_=True)
	results_processed = _dicts_to_lists(results)
	# Create file
	file = _create_file(results_processed)
	return file


def _dicts_to_lists(my_list):
	"""Convert list of dictionaries to list of lists, with first
	nested list containing column names.
	"""
	try:
		column_names = list(my_list[0].keys())
	# Account for tabs without data e.g. no learners have filled out a survey
	except IndexError:
		return [[gettext('Apologies, this tab contains no data.')]]
	results_processed = []
	results_processed.append(column_names)
	for dict_ in my_list:
		# Passing each key to dict is slow as requires each key
		# to be hashed. However, this method is safer than using
		# dict.values as lists produced guaranteed to follow correct
		# order. Note dicts in Python >= 3.6 preserve order.
		new_list = [dict_[column] for column in column_names]
		results_processed.append(new_list)
	return results_processed


def _create_file(my_data):
	"""Create CSV file in memory."""
	file = StringIO()
	csv_writer = csv.writer(file)
	csv_writer.writerows(my_data)
	return file.getvalue()

import pandas as pd
from flask_babel import gettext
from catalogue_app.db import query_mysql


class Comments:
	"""Fetch comments for the API."""
	def __init__(self, lang, course_code, short_question, fiscal_year, stars, start_index):
		self.lang = lang
		self.course_code = course_code
		self.short_question = short_question
		self.fiscal_year = fiscal_year
		self.stars = stars
		self.start_index = start_index
		# Raw data returned by query
		self.raw = None
		# Processed data
		self.processed = None
	
	
	def load(self):
		"""Run query and process raw data."""
		self.raw = self._load_raw()
		self.processed = self._process_raw()
		# Return self to allow method chaining
		print(self.raw)
		return self
	
	
	def _load_raw(self):
		"""Query the DB and extract all comments of a given type for
		self.course_code.
		"""
		field_name = 'offering_city_{0}'.format(self.lang)
		query = """
			SELECT text_answer, learner_classif, {0}, fiscal_year, quarter, stars
			FROM comments
			WHERE
				course_code = %s
				AND
				short_question = %s
				AND
				(fiscal_year = %s OR %s = '')
				AND
				(stars = %s OR %s = '');
		""".format(field_name)
		results = query_mysql(query, (self.course_code, self.short_question,
									  self.fiscal_year, self.fiscal_year,
									  self.stars, self.stars))
		results = pd.DataFrame(results, columns=['text_answer', 'learner_classif', 'offering_city',
												 'fiscal_year', 'quarter', 'stars'])
		# Account for learners who didn't submit stars with their comments
		results['stars'].fillna(0, inplace=True)
		# Return False if course has received no feedback
		return False if results.empty else results
	
	
	def _process_raw(self):
		""" Parse raw data with Pandas and process into form required for API.
		Return False if course has received no comments.
		"""
		# Explicitely checking 'if df is False' rather than 'if not df' as
		# DataFrames do not have a truth value
		if self.raw is False:
			return False
		results_processed = []
		# Unpack tuple as some fields require customization
		for row in self.raw.itertuples(index=False):
			text_answer = row[0]
			# Account for 'Unknown' being 'Inconnu' in FR
			learner_classif = row[1].replace(' - Unknown', '')
			learner_classif = learner_classif.replace('Unknown', 'Inconnu') if self.lang == 'fr' else learner_classif
			# Account for English vs French title formatting
			offering_city = self._format_title(row[2])
			# Use standard fiscal year format e.g. '2018-19' instead of '2018-2019'
			fiscal_year = row[3].replace('-20', '-')
			# Account for e.g. 'Q2' being 'T2' in FR
			quarter = row[4].replace('Q', 'T') if self.lang == 'fr' else row[4]
			stars = int(row[5])
			# Reassemble and append
			tup = (text_answer, learner_classif, offering_city, fiscal_year, quarter, stars)
			results_processed.append(tup)
		return results_processed
	
	
	def _format_title(self, my_string):
		"""Correct English and French formatting edge cases."""
		if self.lang == 'fr':
			s = my_string.title()
			s = s.replace('Région De La Capitale Nationale (Rcn)', 'Région de la capitale nationale (RCN)').replace("'S", "'s")
			return s
		else:
			s = my_string.title()
			s = s.replace('(Ncr)', '(NCR)').replace("'S", "'s")
			return s


class Categorical:
	"""Data for the Categorical section of the Comments tab."""
	def __init__(self, lang, course_code):
		self.lang = lang
		self.course_code = course_code
		# Raw data returned by query
		self.categorical_data = None
		# Processed data
		self.reason = None
		self.technical_bool = None
		self.language_bool = None
		self.gccampus_bool = None
		self.preparation = None
	
	
	def load(self):
		"""Run query and process raw data."""
		self.categorical_data = self._load_all_categorical()
		# Parse with Pandas and process into form required by Highcharts
		self.reason = self._load_categorical('Reason to Participate')
		self.technical_bool = self._load_categorical('Technical Issues')
		self.language_bool = self._load_categorical('OL Available')
		self.gccampus_bool = self._load_categorical('GCcampus Tools Used')
		self.preparation = self._load_categorical('Prep')
		# Return self to allow method chaining
		return self
	
	
	def _load_all_categorical(self):
		"""Query the DB and extract all categorical question data for a given course code."""
		field_name = 'text_answer_fr' if self.lang == 'fr' else 'text_answer'
		query = """
			SELECT short_question, {0}, COUNT({0})
			FROM comments
			WHERE
				course_code = %s
				AND
				short_question IN ('Reason to Participate', 'Technical Issues', 'OL Available', 'GCcampus Tools Used', 'Prep')
			GROUP BY short_question, {0}
			ORDER BY 1 ASC;
		""".format(field_name)
		results = query_mysql(query, (self.course_code,))
		results = pd.DataFrame(results, columns=['short_question', 'text_answer', 'count'])
		# Return False if course has received no feedback
		return False if results.empty else results
	
	
	def _load_categorical(self, question):
		"""Extract and process results for a categorical question from the raw
		data. Returns False if course has received no feedback of that type.
		"""
		# Explicitely checking 'if df is False' rather than 'if not df' as
		# DataFrames do not have a truth value
		if self.categorical_data is False:
			return False
		data_filtered = self.categorical_data.loc[self.categorical_data['short_question'] == question, :]
		results_processed = []
		for row in data_filtered.itertuples(index=False):
			# Unpack tuple as some fields require customization
			answer = row[1]
			count = row[2]
			# Reassemble and append
			dict_ = {'name': answer, 'y': count}
			results_processed.append(dict_)
		return results_processed if results_processed else [{'name': gettext('No response'), 'y': 1}]

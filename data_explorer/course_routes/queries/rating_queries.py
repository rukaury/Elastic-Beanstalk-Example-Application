import pandas as pd
from data_explorer.db import query_mysql


class Ratings:
	"""Data for the Ratings tab."""
	def __init__(self, lang, course_code):
		self.lang = lang
		self.course_code = course_code
		self.data = None
		self.all_ratings = None
	
	
	def load(self):
		"""Run all queries and process all raw data."""
		self._load_ratings()
		self._process_ratings()
		# Return self to allow method chaining
		return self
	
	
	def _load_ratings(self):
		"""Query the DB and extract all ratings data for a given course code."""
		field_name_1 = 'short_question_{0}'.format(self.lang)
		field_name_2 = 'long_question_{0}'.format(self.lang)
		query = """
			SELECT {0}, {1}, month, numerical_answer, count
			FROM ratings
			WHERE course_code = %s
			ORDER BY {0};
		""".format(field_name_1, field_name_2)
		results = query_mysql(query, (self.course_code,))
		results = pd.DataFrame(results, columns=['short_question', 'long_question', 'month', 'average', 'count'])
		# Return False if course has received no feedback
		self.data = False if results.empty else results
	
	
	def _process_ratings(self):
		"""Extract and process results for all possible ratings from the raw data.
		Returns False if course has received no feedback of that type.
		"""
		# Explicitely checking 'if df is False' rather than 'if not df' as
		# DataFrames do not have a truth value
		if self.data is False:
			return False
		# Get list of questions for which the course has answers
		questions = self.data.loc[:, ['short_question', 'long_question']].drop_duplicates(inplace=False)
		# Process into form required by Highcharts
		results_processed = []
		for question in questions.itertuples(index=False):
			short_question = question[0]
			long_question = question[1]
			data_filtered = self.data.loc[self.data['short_question'] == short_question, ['month', 'average', 'count']]
			monthly_values = self._get_monthly_values(data_filtered)
			results_processed.append((short_question, long_question, monthly_values))
		self.all_ratings = results_processed
	
	
	@staticmethod
	def _get_monthly_values(df):
		"""Accepts a Panda's DataFrame with columns ['month', 'average', and 'count'].
		Returns	a list of dicts ensuring all possible months have values. Months
		not listed in DataFrame assigned average and count of 0."""
		months = ['April', 'May', 'June', 'July', 'August', 'September',
				  'October', 'November', 'December', 'January', 'February', 'March']
		monthly_values = []
		for month in months:
			df_month = df.loc[df['month'] == month, :]
			try:
				average = df_month.iloc[0]['average']
				count = df_month.iloc[0]['count']
			except IndexError:
				average = 0
				count = 0
			monthly_values.append({'y': average, 'count': count})
		return monthly_values

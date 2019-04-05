from flask import Blueprint, jsonify, request
from catalogue_app import auth
from catalogue_app.course_routes import utils
from catalogue_app.course_routes.queries import comment_queries

# Instantiate blueprint
api = Blueprint('api', __name__)


@api.route('/api/v1/comments/<string:comment_type>/<string:course_code>')
@auth.login_required
def comments(comment_type, course_code):
	"""Return all comments of a given type (e.g. general comments) for a
	given course code."""
	# Only allow 'en' and 'fr' to be passed to app
	VALID_LANGS = ['en', 'fr']
	
	# Prioritize query string, else cookie user has already set,
	# else default to English
	query_string_lang = request.args.get('lang', None)
	cookie_lang = request.cookies.get('lang', None)
	if query_string_lang in VALID_LANGS:
		lang = query_string_lang
	elif cookie_lang in VALID_LANGS:
		lang = cookie_lang
	else:
		lang = 'en'
	
	# Validate user input
	# Avoid use of Flask Babel gettext in this module to allow
	# query string to override cookie 'lang'
	course_code = utils.validate_course_code({'course_code': course_code}, 'this_year')
	if not course_code:
		if lang == 'fr':
			error_message = 'Erreur : Cours introuvable'
		else:
			error_message = 'Error: Course Not Found'
		return jsonify(error_message)
	
	# Instantiate class Comments
	comments = comment_queries.Comments(lang, course_code).load()
	if comment_type == 'general':
		results = comments.general
	elif comment_type == 'technical':
		results = comments.technical
	elif comment_type == 'language':
		results = comments.language
	elif comment_type == 'performance':
		results = comments.performance
	elif comment_type == 'instructor':
		if lang == 'fr':
			error_message = 'Erreur : Les commentaires concernant les instructeurs sont présentement désactivés à cause des restrictions de confidentialité.'
		else:
			error_message = 'Error: Comments on instructor performance are currently disabled due to privacy restrictions.'
		return jsonify(error_message), 410
	else:
		if lang == 'fr':
			error_message = 'Erreur : Les commentaires de ce genre ne sont présentement pas recueillis dans nos sondages.'
		else:
			error_message = 'Error: Comments of this type are not currently collected in our surveys.'
		return jsonify(error_message), 404
	results = [_make_dict(lang, result) for result in results]
	return jsonify(results)


def _make_dict(lang, my_tup):
	"""Make tuple in a dictionary so can be jsonified into
	an object.
	"""
	if lang == 'fr':
		labels = ['texte_du_commentaire', 'étoiles', 'classification_de_l_apprenant',
				  'ville_de_l_offre', 'année_fiscale_de_l_offre', 'trimestre_de_l_offre']
	else:
		labels = ['comment_text', 'stars', 'learner_classification', 'offering_city',
				  'offering_fiscal_year', 'offering_quarter']	
	results = {key: val for key, val in zip(labels, my_tup)}
	return results

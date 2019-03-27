from flask import Blueprint, render_template, request
from catalogue_app import auth
from catalogue_app.config import Config
from catalogue_app.course_routes import utils
from catalogue_app.course_routes.forms import course_form
from catalogue_app.course_routes.queries import (
	comment_queries, dashboard_learner_queries, dashboard_offering_queries,
	explore_queries, general_queries, map_queries, rating_queries
)

# Instantiate blueprint
course = Blueprint('course', __name__)


# Make LAST_YEAR and THIS_YEAR available to all templates
LAST_YEAR = Config.LAST_YEAR
THIS_YEAR = Config.THIS_YEAR
@course.context_processor
def context_processor():
	return {'LAST_YEAR': LAST_YEAR.replace('_', '-'), 'THIS_YEAR': THIS_YEAR.replace('_', '-')}


# Home page with search bar
@course.route('/home')
@auth.login_required
def home():
	# Only allow 'en' and 'fr' to be passed to app
	lang = 'fr' if request.cookies.get('lang', None) == 'fr' else 'en'
	form = course_form(lang, THIS_YEAR)()
	return render_template('index.html', form=form)


# Catalogue's entry for a given course: the meat & potatoes of the app
@course.route('/course-result')
@auth.login_required
def course_result():
	# Only allow 'en' and 'fr' to be passed to app
	lang = 'fr' if request.cookies.get('lang', None) == 'fr' else 'en'
	# Security check: if course_code doesn't exist, render not_found.html
	course_code = utils.validate_course_code(request.args, THIS_YEAR)
	if not course_code:
		return render_template('not-found.html')
	
	# Instantiate classes
	course_info = general_queries.CourseInfo(lang, course_code).load()
	overall_numbers_LY = dashboard_offering_queries.OverallNumbers(LAST_YEAR, course_code).load()
	overall_numbers_TY = dashboard_offering_queries.OverallNumbers(THIS_YEAR, course_code).load()
	offering_locations = dashboard_offering_queries.OfferingLocations(lang, THIS_YEAR, course_code).load()
	learners = dashboard_learner_queries.Learners(lang, THIS_YEAR, course_code).load()
	map = map_queries.Map(THIS_YEAR, course_code).load()
	# ratings = rating_queries.Ratings(lang, course_code).load()
	comments = comment_queries.Comments(lang, course_code).load()
	
	pass_dict = {
		#Global
		'course_code': course_code,
		'course_title': learners.course_title,
		# General
		'course_info': course_info.course_info,
		# Dashboard - offerings
		'overall_numbers_LY': overall_numbers_LY.counts,
		'overall_numbers_TY': overall_numbers_TY.counts,
		'region_drilldown': offering_locations.regions,
		'province_drilldown': offering_locations.provinces,
		'city_drilldown': offering_locations.cities,
		'offerings_per_lang_LY': dashboard_offering_queries.offerings_per_lang(LAST_YEAR, course_code),
		'offerings_per_lang_TY': dashboard_offering_queries.offerings_per_lang(THIS_YEAR, course_code),
		'offerings_cancelled_global_LY': dashboard_offering_queries.offerings_cancelled_global(LAST_YEAR),
		'offerings_cancelled_global_TY': dashboard_offering_queries.offerings_cancelled_global(THIS_YEAR),
		'offerings_cancelled_LY': dashboard_offering_queries.offerings_cancelled(LAST_YEAR, course_code),
		'offerings_cancelled_TY': dashboard_offering_queries.offerings_cancelled(THIS_YEAR, course_code),
		'avg_class_size_global_LY': dashboard_offering_queries.avg_class_size_global(LAST_YEAR),
		'avg_class_size_global_TY': dashboard_offering_queries.avg_class_size_global(THIS_YEAR),
		'avg_class_size_LY': dashboard_offering_queries.avg_class_size(LAST_YEAR, course_code),
		'avg_class_size_TY': dashboard_offering_queries.avg_class_size(THIS_YEAR, course_code),
		'avg_no_shows_global_LY': round(dashboard_offering_queries.avg_no_shows_global(LAST_YEAR), 1),
		'avg_no_shows_global_TY': round(dashboard_offering_queries.avg_no_shows_global(THIS_YEAR), 1),
		'avg_no_shows_LY': round(dashboard_offering_queries.avg_no_shows(LAST_YEAR, course_code), 1),
		'avg_no_shows_TY': round(dashboard_offering_queries.avg_no_shows(THIS_YEAR, course_code), 1),
		# Dashboard - learners
		'regs_per_month': learners.regs_per_month,
		'top_5_depts': learners.top_depts,
		'top_5_classifs': learners.top_classifs,
		# Maps
		'offering_city_counts': map.offerings,
		'learner_city_counts': map.learners,
		# Ratings
		# 'all_ratings': ratings.all_ratings,
		# Comments
		'general_comments': comments.general,
		'technical_comments': comments.technical,
		'language_comments': comments.language,
		'performance_comments': comments.performance,
		# Categorical and yes/no questions
		'reason_to_participate': comments.reason,
		'technical_issues': comments.technical_bool,
		'languages_available': comments.language_bool,
		'tools_used': comments.gccampus_bool,
		'prepared_by': comments.preparation
	}
	return render_template('/course-page/main.html', pass_dict=pass_dict)


# Explore
@course.route('/explore')
@auth.login_required
def explore():
	# Only allow 'en' and 'fr' to be passed to app
	lang = 'fr' if request.cookies.get('lang', None) == 'fr' else 'en'
	course_list = explore_queries.CourseList(lang, THIS_YEAR).load()
	pass_dict = course_list._get_nested_dicts()
	return render_template('explore/explore.html', pass_dict=pass_dict)

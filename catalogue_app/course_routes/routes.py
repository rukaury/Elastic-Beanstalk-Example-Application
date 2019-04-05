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


# Make certain config vars available to all templates
LAST_YEAR = Config.LAST_YEAR
THIS_YEAR = Config.THIS_YEAR
GOOGLE_MAPS_API_KEY = Config.GOOGLE_MAPS_API_KEY
@course.context_processor
def context_processor():
	return {
		'LAST_YEAR': LAST_YEAR,
		'THIS_YEAR': THIS_YEAR,
		'GOOGLE_MAPS_API_KEY': GOOGLE_MAPS_API_KEY
	}


# Home page with search bar
@course.route('/home')
@auth.login_required
def home():
	# Only allow 'en' and 'fr' to be passed to app
	lang = 'fr' if request.cookies.get('lang', None) == 'fr' else 'en'
	form = course_form(lang, 'this_year')()
	return render_template('index.html', form=form)


# Catalogue's entry for a given course: the meat & potatoes of the app
@course.route('/course-result')
@auth.login_required
def course_result():
	# Only allow 'en' and 'fr' to be passed to app
	lang = 'fr' if request.cookies.get('lang', None) == 'fr' else 'en'
	# Security check: if course_code doesn't exist, render not_found.html
	course_code = utils.validate_course_code(request.args, 'this_year')
	if not course_code:
		return render_template('not-found.html')
	
	# Instantiate classes
	course_info = general_queries.CourseInfo(lang, course_code).load()
	overall_offering_numbers_LY = dashboard_offering_queries.OverallOfferingNumbers('last_year', course_code).load()
	overall_offering_numbers_TY = dashboard_offering_queries.OverallOfferingNumbers('this_year', course_code).load()
	offering_locations = dashboard_offering_queries.OfferingLocations(lang, 'this_year', course_code).load()
	overall_learner_numbers_LY = dashboard_learner_queries.OverallLearnerNumbers('last_year', course_code).load()
	overall_learner_numbers_TY = dashboard_learner_queries.OverallLearnerNumbers('this_year', course_code).load()
	learners = dashboard_learner_queries.Learners(lang, 'this_year', course_code).load()
	map = map_queries.Map('this_year', course_code).load()
	# ratings = rating_queries.Ratings(lang, course_code).load()
	comments = comment_queries.Comments(lang, course_code).load()
	
	pass_dict = {
		#Global
		'course_code': course_code,
		'course_title': learners.course_title,
		'business_type': learners.business_type,
		# General
		'course_info': course_info.course_info,
		# Dashboards - Offerings
		'overall_offering_numbers_LY': overall_offering_numbers_LY.counts,
		'overall_offering_numbers_TY': overall_offering_numbers_TY.counts,
		'region_drilldown': offering_locations.regions,
		'province_drilldown': offering_locations.provinces,
		'city_drilldown': offering_locations.cities,
		'offerings_per_lang_LY': dashboard_offering_queries.offerings_per_lang('last_year', course_code),
		'offerings_per_lang_TY': dashboard_offering_queries.offerings_per_lang('this_year', course_code),
		'offerings_cancelled_global_LY': dashboard_offering_queries.offerings_cancelled_global('last_year'),
		'offerings_cancelled_global_TY': dashboard_offering_queries.offerings_cancelled_global('this_year'),
		'offerings_cancelled_LY': dashboard_offering_queries.offerings_cancelled('last_year', course_code),
		'offerings_cancelled_TY': dashboard_offering_queries.offerings_cancelled('this_year', course_code),
		'avg_class_size_global_LY': dashboard_offering_queries.avg_class_size_global('last_year'),
		'avg_class_size_global_TY': dashboard_offering_queries.avg_class_size_global('this_year'),
		'avg_class_size_LY': dashboard_offering_queries.avg_class_size('last_year', course_code),
		'avg_class_size_TY': dashboard_offering_queries.avg_class_size('this_year', course_code),
		'avg_no_shows_global_LY': round(dashboard_offering_queries.avg_no_shows_global('last_year'), 1),
		'avg_no_shows_global_TY': round(dashboard_offering_queries.avg_no_shows_global('this_year'), 1),
		'avg_no_shows_LY': round(dashboard_offering_queries.avg_no_shows('last_year', course_code), 1),
		'avg_no_shows_TY': round(dashboard_offering_queries.avg_no_shows('this_year', course_code), 1),
		# Dashboards - Learners
		'overall_learner_numbers_LY': overall_learner_numbers_LY.counts,
		'overall_learner_numbers_TY': overall_learner_numbers_TY.counts,
		'regs_per_month': learners.regs_per_month,
		'no_shows_per_month': learners.no_shows_per_month,
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
		# Comments - Other
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
	course_list = explore_queries.CourseList(lang, 'this_year').load()
	pass_dict = course_list._get_nested_dicts()
	return render_template('explore/explore.html', pass_dict=pass_dict)

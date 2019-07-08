from flask import Blueprint, make_response, render_template, redirect, request, url_for
# from data_explorer import auth

main = Blueprint('main', __name__)


@main.route('/')
def splash():
    return render_template('splash.html')


@main.route('/about')
@auth.login_required
def about():
    return render_template('about.html')


# Coming soon
@main.route('/departments')
@auth.login_required
def departments():
    return render_template('departments.html')


@main.route('/setlang')
@auth.login_required
def setlang():
    """Allow pages to set cookie 'lang' via query string."""
    # Redirect pages back to themselves except for splash
    if request.referrer.endswith('/'):
        resp = make_response(redirect(url_for('course.home')))
    else:
        resp = make_response(redirect(request.referrer))
    # Only allow 'en' and 'fr' to be passed to app
    if 'lang' in request.args:
        if request.args['lang'] == 'fr':
            resp.set_cookie('lang', 'fr')
        # If 'en' or junk is passed, default to 'en'
        else:
            resp.set_cookie('lang', 'en')
    return resp

from flask import Blueprint, render_template

errors = Blueprint('errors', __name__, template_folder='templates')


@errors.app_errorhandler(404)
def error_404(error_message):
    return render_template('404.html', error_message=error_message), 404

@errors.app_errorhandler(403)
def error_403(error_message):
    return render_template('403.html', error_message=error_message), 403

@errors.app_errorhandler(500)
def error_500(error_message):
    return render_template('500.html', error_message=error_message), 500

from flask import render_template
from app.main import bp

@bp.app_errorhandler(404)
def not_found_error(error):
    """
    Handles 404 Not Found errors for the entire application.
    """
    return render_template('errors/404.html'), 404

@bp.app_errorhandler(500)
def internal_error(error):
    """
    Handles 500 Internal Server Error for the entire application.
    """
    return render_template('errors/500.html'), 500
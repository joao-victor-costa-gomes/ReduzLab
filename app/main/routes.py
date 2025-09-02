from flask import render_template
from app.main import bp

# home page of the application
@bp.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')
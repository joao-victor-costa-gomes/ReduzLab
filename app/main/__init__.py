from flask import Blueprint

bp = Blueprint('main', __name__)

from app.main import routes, errors

# algorithm routes
from app.main.algorithm_routes import pca_route
from app.main.algorithm_routes import tsne_route
from app.main.algorithm_routes import lda_route
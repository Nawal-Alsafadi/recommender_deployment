from flask import Blueprint

# from controllers.popularity.train_popularity_recommend import train_popularity_recommend
from api.controllers.popularity.recommends_popularity import get_popularity_recommends

products_recommend_bp = Blueprint('products_recommend_bp', __name__)

products_recommend_bp.route('recommendation/products', methods=['GET'])(get_popularity_recommends)
# products_recommend_bp.route('recommendation/train-products', methods=['POST'])(train_popularity_recommend)
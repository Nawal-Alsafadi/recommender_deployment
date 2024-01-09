from flask import Blueprint

# from controllers.popularity.train_popularity_recommend import train_popularity_recommend
from api.controllers.popularity.recommends_popularity import get_popularity_recommends, get_popularity_recommends_d
from api.controllers.popularity.train_popularity_recommend import train_popularity_recommend_d

popularity_recommend_bp = Blueprint('popularity_bp', __name__)
popularity_recommend_bp.route('recommendation/popularity', methods=['GET'])(get_popularity_recommends)
# popularity_recommend_bp.route('recommendation/train-popularity', methods=['POST'])(train_popularity_recommend)
popularity_recommend_bp.route('recommendation/train-popularity-d', methods=['POST'])(train_popularity_recommend_d)

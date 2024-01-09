from flask import Blueprint
from api.controllers.collaborative.recommends_collaborative import get_collaborative_recommends
# from controllers.collaborative.train_collaborative import train_collaborative_recommender
from api.controllers.collaborative.train_collaborative import train_collaborative_recommender_d

collaborative_recommend_bp = Blueprint('collaborative_bp', __name__)
collaborative_recommend_bp.route('recommendation/collaborative', methods=['GET'])(get_collaborative_recommends)
# collaborative_recommend_bp.route('recommendation/train-collaborative', methods=['POST'])(train_collaborative_recommender)
collaborative_recommend_bp.route('recommendation/train-collaborative-d', methods=['POST'])(train_collaborative_recommender_d)

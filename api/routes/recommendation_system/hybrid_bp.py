from flask import Blueprint
from api.controllers.hybrid.hyprid_train import  train_hybrid_recommender_d
from api.controllers.hybrid.hyprid_recommends import get_hybrid_recommends

hybrid_recommend_bp = Blueprint('hybrid_bp', __name__)
hybrid_recommend_bp.route('recommendation/hybrid', methods=['GET'])(get_hybrid_recommends)
# hybrid_recommend_bp.route('recommendation/train-hybrid', methods=['POST'])(train_hybrid_recommender)
hybrid_recommend_bp.route('recommendation/train-hybrid-d', methods=['POST'])(train_hybrid_recommender_d)

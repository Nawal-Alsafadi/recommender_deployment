import pandas as pd
from flask import request, jsonify, make_response
from api.middle_wares.num_recommends_params import extract_num_recommends_params
from api.middle_wares.user_id_params import extract_user_id_params
from api.models.recommendation_model.main_recommendation_model.stage_advanved.collaborative_recommender import \
    CollaborativeRecommender

@extract_num_recommends_params
@extract_user_id_params
def get_collaborative_recommends(user_id, num_recommendations):
    try:
        collaborative_recommender = CollaborativeRecommender()
        data = collaborative_recommender.read_results()
        result = CollaborativeRecommender.recommend_items(user_id=user_id, predictions=data, num_recommendations=num_recommendations )
        return make_response(jsonify({
            "message": "Recommendation completed successfully.",
            "success": True,
            "products_ids": result
        })), 200
    except Exception as e:
        print(e)
        return make_response(jsonify({
            "message": "something went wrong, we're working to solve it",
            "success": False
        })), 500

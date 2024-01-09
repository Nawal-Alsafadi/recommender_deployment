from flask import jsonify, make_response
# from controllers.collaborative.train_collaborative import train_collaborative_recommender
from api.models.recommendation_model.main_recommendation_model.stage_advanved.hybrid_recommender import HybridRecommender
from api.middle_wares.recommenders_middleware.hybrid_middleware import train_hybrid_payload
import logging

def train_hybrid_recommender_common(hybrid_recommender, data):
    """
    Common logic for training the hybrid recommender.

    Args:
        hybrid_recommender: An instance of HybridRecommender.
        data: Training data.

    """
    try:
        similarity_df = hybrid_recommender.train(data=data)
        hybrid_recommender.save_results(similarity_df=similarity_df)
        return make_response(jsonify({
            "message": "Training completed successfully",
            "success": True
        })), 201
    except Exception as e:
        logging.error(f"Error during hybrid model training: {str(e)}")
        return make_response(jsonify({
            "message": "Something went wrong. We're working to solve it (hybrid model)",
            "success": False
        })), 500

@train_hybrid_payload
def train_hybrid_recommender_d(clear_data: bool, user_column, item_column, rating_column, attribute_column, csv_path):
    """
    Train the hybrid recommender with specified parameters and data path.

    Args:
        clear_data (bool): Flag indicating whether to clear existing data.
        user_column: Name of the user column in the CSV file (from the path ).
        item_column: Name of the item column in the CSV file (from the path ).
        rating_column: Name of the rating column in the CSV file (from the path ).
        attribute_column: Name of the attribute column in the CSV file (from the path ).
        csv_path: Path to the CSV file containing training data.


    """
    try:
        # train_collaborative_recommender()
        hybrid_recommender = HybridRecommender(
            user_column=user_column, item_column=item_column, rating_column=rating_column, attribute_column=attribute_column
        )
        data = hybrid_recommender.read_data(csv_path=csv_path)
        return train_hybrid_recommender_common(hybrid_recommender, data)
    except Exception as e:
        logging.error(f"Error during hybrid model training: {str(e)}")
        return make_response(jsonify({
            "message": "Something went wrong. We're working to solve it (hybrid model)",
            "success": False
        })), 500

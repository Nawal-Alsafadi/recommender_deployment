import logging
from flask import jsonify, make_response
from api.models.recommendation_model.main_recommendation_model.stage_advanved.collaborative_recommender import CollaborativeRecommender
from api.middle_wares.recommenders_middleware.collaborative_middleware import train_collaborative_payload

def train_collaborative_recommender_common(collaborative_recommender, data):
    """
    Common logic for collaborative recommender training.

    Args:
        collaborative_recommender: An instance of CollaborativeRecommender.
        data: Training data.

    """
    try:
        predictions_df = collaborative_recommender.train(data=data)
        collaborative_recommender.save_results(predictions_df=predictions_df)
        return make_response(jsonify({
            "message": "Training collaborative model completed successfully",
            "success": True
        })), 201
    except Exception as e:
        logging.error(f"Error during collaborative model training: {str(e)}")
        return make_response(jsonify({
            "message": "Something went wrong. We're working to solve it (collaborative model)",
            "success": False
        })), 500



@train_collaborative_payload
def train_collaborative_recommender_d(clear_data: bool, user_column, item_column, rating_column, csv_path):
    """
    Train the collaborative recommender with specified parameters and data path.

    Args:
        clear_data (bool): Flag indicating whether to clear existing data.
        user_column: Name of the user column in the  CSV file (from the path ).
        item_column: Name of the item column in the CSV file (from the path ).
        rating_column: Name of the rating column in the CSV file (from the path ).
        csv_path: Path to the CSV file containing training data.

    """
    try:
        collaborative_recommender = CollaborativeRecommender(
            user_column=user_column, item_column=item_column, rating_column=rating_column
        )
        data = collaborative_recommender.read_data(csv_path=csv_path)
        return train_collaborative_recommender_common(collaborative_recommender, data)
    except Exception as e:
        logging.error(f"Error during collaborative model training: {str(e)}")
        return make_response(jsonify({
            "message": "Something went wrong. We're working to solve it (collaborative model)",
            "success": False
        })), 500

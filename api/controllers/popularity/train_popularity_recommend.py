from flask import jsonify, make_response
from api.controllers.pandas_file_controller import PandasDf
from api.models.recommendation_model.main_recommendation_model.popularity_model import PopularRecommendation
from api.utils.paths import Paths
from api.middle_wares.recommenders_middleware.popular_middleware import train_popular_payload
import logging




@train_popular_payload
def train_popularity_recommend_d(clear_data: bool, user_column, item_column, rating_column, csv_path):
    """
    Train the popularity recommendation model with specified parameters and data path.

    Args:
        clear_data (bool): Flag indicating whether to clear existing data.
        user_column: Name of the user column in the CSV file (from the path).
        item_column: Name of the item column in the CSV file (from the path).
        rating_column: Name of the rating column in the CSV file (from the path).
        csv_path: Path to the CSV file containing training data.

    """
    try:
        logging.info("Training popularity recommendation model.")
        
        # Read CSV data
        data = PandasDf.read_csv(path=csv_path)
        logging.info("CSV data loaded successfully.")
        
        # Instantiate PopularRecommendation
        popularity_recommendation = PopularRecommendation(
            train_data=data, user_column=user_column, item_column=item_column, rating_column=rating_column
        )
        
        # Create popularity DataFrame
        popularity_df = popularity_recommendation.create()
        
        # Write results to CSV
        paths = Paths()
        PandasDf.write_csv(path=paths.popularityRecommendation, df=popularity_df)
        
        return make_response(jsonify({
            "message": "Training completed successfully.",
            "success": True
        })), 201
    except Exception as e:
        logging.error(f"Error during popularity model training: {str(e)}")
        return make_response(jsonify({
            "message": "Something went wrong. We're working to solve it (popularity model)",
            "success": False
        })), 500

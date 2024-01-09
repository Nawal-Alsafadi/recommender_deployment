from flask import make_response, jsonify, request

from api.controllers.pandas_file_controller import PandasDf
from api.middle_wares.num_recommends_params import extract_num_recommends_params
from api.middle_wares.user_id_params import extract_user_id_params

from api.models.recommendation_model.main_recommendation_model.popularity_model import PopularRecommendation, number_of_product_ratings, \
    average_product_rating
from api.utils.paths import Paths


@extract_user_id_params
@extract_num_recommends_params
def get_popularity_recommends(num_recommendations, user_id):
    try:

        paths = Paths()
        popularity_df = PandasDf.read_csv(path=paths.popularityRecommendation)

        results = popularity_df[
            [
                "productId",
                number_of_product_ratings,
                average_product_rating,
                "score",
            ]
        ].head(num_recommendations)
        return make_response(jsonify({
            "message": "Recommendation completed successfully.",
            "success": True,
            "products_ids": results["productId"].values.tolist()
        })), 200

    except Exception as e:
        return make_response(jsonify({
            "message": "something went wrong, we're working to solve it",
            "success": False
        })), 500

@extract_user_id_params
@extract_num_recommends_params
def get_popularity_recommends_d(num_recommendations, user_id):
    try:
        paths = Paths()

        trainData = PandasDf.read_csv(path = paths.popularityTrain)
        popularity_recommender = PopularRecommendation(train_data=trainData)
        data = PandasDf.read_csv(path=paths.popularityRecommendation)

        result1 = popularity_recommender.recommend_items(data,num_recommendations =num_recommendations  )

        return make_response(jsonify({
            "message": "Recommendation completed successfully.",
            "success": True,
            "products_ids": result1
        })), 200

    except Exception as e:
        return make_response(jsonify({
            "message": "something went wrong, we're working to solve it",
            "success": False
        })), 500

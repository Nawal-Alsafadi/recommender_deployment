from functools import wraps

from flask import request, make_response, jsonify


def extract_num_recommends_params(next_to):
    @wraps(next_to)
    def wrapper(*args, **kwargs):
        num_recommendations = request.json.get('num_recommendations', 10)
        try:
            num_recommendations = int(num_recommendations)
        except ValueError:
            return make_response(jsonify({
                "message": "num_recommendations must be number.",
                "success": False
            })), 400
        request.num_recommendations = num_recommendations
        return next_to(num_recommendations=num_recommendations, *args, **kwargs)

    return wrapper

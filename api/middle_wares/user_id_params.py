from functools import wraps

from flask import make_response, jsonify, request


def extract_user_id_params(next_to):
    @wraps(next_to)
    def wrapper(*args, **kwargs):
        user_id = request.json.get('user_id')
        if user_id is None:
            return make_response(jsonify({
                "message": "user_id is required.",
                "success": False
            })), 406
        try:
            user_id = int(user_id)
        except ValueError:
            return make_response(jsonify({
                "message": "user_id must be number.",
                "success": False
            })), 400
        return next_to(user_id=user_id, *args, **kwargs)

    return wrapper

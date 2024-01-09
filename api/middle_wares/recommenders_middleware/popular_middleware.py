from functools import wraps
import logging
import os

from flask import make_response, jsonify, request
from api.utils.parse_requests import pares_post_request

def train_popular_payload(next_to):
    """
    Middleware for training popular models.

    This middleware parses the POST request, extracts relevant parameters,
    validates them, normalizes the CSV path, and checks if the path exists.
    If successful, it calls the next function in the pipeline with the
    extracted parameters.

    Args:
        next_to (function): The next function in the pipeline.

    Returns:
        function: The wrapped middleware function.
    """
    @wraps(next_to)
    def wrapper(*args, **kwargs):
        # Parse the POST request data
        data = pares_post_request(request=request)

        # Extract relevant information from the parsed data
        clear_data = data.get("clear_previous_analysis", True)
        user_column = data.get("user_column")
        item_column = data.get("item_column")
        rating_column = data.get("rating_column")
        csv_path = data.get("csv_path")

        # Validate the input parameters
        if not isinstance(clear_data, bool):
            return make_response(jsonify({
                "message": "clear_previous_analysis must be boolean",
                "success": False
            })), 406
        if not user_column or not item_column or not rating_column or not csv_path:
            return make_response(jsonify({
                "message": "user_column, item_column, rating_column, and csv_path are required",
                "success": False
            })), 400

        try:
            # Use os.path.normpath to normalize the path
            csv_path = os.path.normpath(csv_path)
            # Log the normalized path
            logging.info(f"Normalized path: {csv_path}")

            # Use os.path.abspath to get the absolute path
            csv_path = os.path.abspath(csv_path)
            # Log the absolute path
            logging.info(f"Absolute path: {csv_path}")

            # Check if the path exists
            if not os.path.exists(csv_path):
                raise FileNotFoundError(f"Path does not exist: {csv_path}")

        except FileNotFoundError as e:
            # Log the error on the server side
            logging.error(f"FileNotFoundError: {str(e)}")

            # Return an error response
            return make_response(jsonify({
                "message": "File not found or path is invalid.",
                "success": False
            })), 404

        except Exception as e:
            # Log the error on the server side
            logging.error(f"Error handling the path: {str(e)}")

            # Return a more generic error response
            return make_response(jsonify({
                "message": "An error occurred while processing the request.",
                "success": False
            })), 500

        # Call the next function in the pipeline with the extracted parameters
        return next_to(clear_data=clear_data, user_column=user_column, item_column=item_column, rating_column=rating_column, csv_path=csv_path, *args, **kwargs)

    return wrapper

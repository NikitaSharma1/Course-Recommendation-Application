from werkzeug.exceptions import HTTPException
from flask import make_response, jsonify
import json


class NotFoundError(HTTPException):
    def __init__(self, status_code, message="NOT FOUND"):
        if status_code == 409:
            message = "already exists"
        if status_code == 404:
            message = "NOT FOUND"
        self.response = make_response(jsonify(message), status_code)
        self.response.headers['Content-Type'] = 'application/json'


class NotGivenError(HTTPException):
    def __init__(self, status_code, error_code, error_message):
        message = {"error_code": error_code, "error_message": error_message}
        self.response = make_response(jsonify(message), status_code)
        self.response.headers['Content-Type'] = 'application/json'

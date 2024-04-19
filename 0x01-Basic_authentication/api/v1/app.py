#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None

if os.getenv('AUTH_TYPE') == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
else:
    auth = Auth()


@app.before_request
def check_auth():
    """checks for user authentication for certain routes"""
    if auth is None:
        return
    excluded_paths = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/'
    ]
    requires_auth = auth.require_auth(request.path, excluded_paths)
    if requires_auth is False:
        return
    auth_header = auth.authorization_header(request)
    if auth_header is None:
        abort(401)
    crnt_user = auth.current_user(request)
    if crnt_user is None:
        abort(403)


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """unauthorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)

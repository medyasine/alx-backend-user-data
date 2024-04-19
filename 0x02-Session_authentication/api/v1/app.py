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


if os.getenv('AUTH_TYPE') == 'session_db_auth':
    from api.v1.auth.session_db_auth import SessionDBAuth
    auth = SessionDBAuth()
elif os.getenv('AUTH_TYPE') == 'session_exp_auth':
    from api.v1.auth.session_exp_auth import SessionExpAuth
    auth = SessionExpAuth()
elif os.getenv('AUTH_TYPE') == 'session_auth':
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()
elif os.getenv('AUTH_TYPE') == 'basic_auth':
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
        '/api/v1/forbidden/',
        '/api/v1/auth_session/login/'
    ]
    requires_auth = auth.require_auth(request.path, excluded_paths)
    if requires_auth is False:
        return
    session_cookie = auth.session_cookie(request)
    auth_header = auth.authorization_header(request)
    if auth_header is None and session_cookie is None:
        abort(401)
    crnt_user = auth.current_user(request)
    request.current_user = crnt_user
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

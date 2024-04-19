#!/usr/bin/env python3
""" Module of Session Auth views
"""
from api.v1.views import app_views
from api.v1.auth.session_auth import SessionAuth
from flask import request, jsonify, abort
from models.user import User
import os


@app_views.route('/auth_session/login',
                 methods=['POST'],
                 strict_slashes=False)
def session_auth():
    """User login after authentication"""
    email = request.form.get('email')
    if not email or len(email) == 0:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if not password or len(password) == 0:
        return jsonify({"error": "password missing"}), 400

    user = None

    users_list = User.search({'email': email})
    if not users_list:
        return jsonify({"error": "no user found for this email"}), 404

    for users in users_list:
        if users.is_valid_password(password):
            user = users

    if not user:
        return jsonify({"error": "wrong password"}), 401

    else:
        from api.v1.app import auth
        user_id = user.id
        session_id = auth.create_session(user_id)
        session_name = os.getenv('SESSION_NAME')
        user_json_data = jsonify(user.to_json())
        user_json_data.set_cookie(session_name, session_id)
        return user_json_data


@app_views.route('/auth_session/logout',
                 methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """logs out a user and destroys its session"""
    from api.v1.app import auth
    destroying_session = auth.destroy_session(request)
    if destroying_session is False:
        abort(404)

    return jsonify({}), 200

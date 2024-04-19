#!/usr/bin/env python3
"""Defining a class Auth"""
from flask import request
from typing import List, TypeVar
import os


User = TypeVar('User')


class Auth:
    """Class Auth that handles Authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require_auth method that returns false if path is
        not in excluded_paths"""
        if (path is None
                or excluded_paths is None
                or len(excluded_paths) == 0):
            return True

        for ex_path in excluded_paths:
            if ex_path[-1] == '*':
                if path[:len(ex_path) - 1] == ex_path[:-1]:
                    return False

        if path[-1] != '/':
            path = path + '/'
        return False if path in excluded_paths else True

    def authorization_header(self, request=None) -> str:
        """authorization_header method"""
        if request is None:
            return None
        auth_value = request.headers.get('Authorization')
        if auth_value is None:
            return None
        else:
            return auth_value

    def current_user(self, request=None) -> User:
        """current_user method"""
        return None

    def session_cookie(self, request=None):
        """return the value of cookie in a get request"""
        if request is None:
            return None

        cookie_name = os.getenv('SESSION_NAME')
        cookie_value = request.cookies.get(cookie_name)
        return cookie_value

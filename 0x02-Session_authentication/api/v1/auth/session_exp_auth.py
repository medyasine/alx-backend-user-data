#!/usr/bin/env python3
"""Defining a class SessionExpAuth"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
import os


class SessionExpAuth(SessionAuth):
    """Class SessionExpAuth that inherits from SessionAuth"""
    def __init__(self) -> None:
        """Initializes a new SessionExpAuth"""
        if os.getenv('SESSION_DURATION'):
            self.session_duration = int(os.getenv('SESSION_DURATION'))
        else:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """creates a session for a user"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        session_info = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_info
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """returns a user_id from a session_id"""
        if session_id is None:
            return None

        users_info = self.user_id_by_session_id.get(session_id)
        if users_info is None:
            return None

        if self.session_duration <= 0:
            return users_info['user_id']

        if 'created_at' not in users_info.keys():
            return None

        if (users_info['created_at']
                + timedelta(seconds=self.session_duration) < datetime.now()):
            return None

        return users_info['user_id']

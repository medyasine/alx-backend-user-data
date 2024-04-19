#!/usr/bin/env python3
"""Defining a class SessionDBAuth"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """class SessionDBAuth that inherits from SessionExpAuth"""
    def create_session(self, user_id=None):
        """creates a session instance for a user"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        session = UserSession(user_id=user_id, session_id=session_id)
        session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """returns a user_id from a session_id on the db"""
        user_session = UserSession.search({'session_id': session_id})
        if not user_session:
            return None

        return user_session[0].user_id

    def destroy_session(self, request=None):
        """destroys and deletes a session instance if exists"""
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False

        user_session = UserSession.search({'session_id': session_id})
        if not user_session:
            return False

        user_session[0].remove()
        return True

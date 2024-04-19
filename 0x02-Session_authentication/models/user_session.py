#!/usr/bin/env python3
"""Defining a model UserSession"""
from models.base import Base


class UserSession(Base):
    """Class UserSession that inherits From Base"""
    def __init__(self, *args: list, **kwargs: dict):
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')

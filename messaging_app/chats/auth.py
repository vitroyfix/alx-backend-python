# messaging_app/chats/auth.py
from rest_framework.simplejwt.authentication import JWTAuthentication

class SimpleJWTAuth(JWTAuthentication):
    """
    Thin wrapper around JWTAuthentication — use this if you want to customize
    token retrieval/validation in one place later.
    """
    pass

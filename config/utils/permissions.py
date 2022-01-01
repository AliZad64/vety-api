from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from ninja.security import HttpBearer

from .schemas import TokenAuth
from django.conf import settings
from jose import jwt, JWTError

ALGORITHM = "HS256"
access_token_jwt_subject = "access"


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire, "sub": access_token_jwt_subject})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)


def create_token(user_id):
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            data={"id": str(user_id.id)}, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


def get_current_user(token: str):
    """ Check auth user
    """
    try:
        print("test")
        payload = jwt.decode(token = token, key = settings.SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        token_data = TokenAuth(**payload)
        print(token_data)
    except JWTError:
        return None

    token_exp = datetime.fromtimestamp(int(token_data.exp))
    if token_exp < datetime.utcnow():
        return None

    return get_object_or_404(get_user_model(), id=token_data.id)


class AuthBearer(HttpBearer):
    def authenticate(self, request, token: str) -> get_user_model:
        print("bye")
        print(token)
        user = get_current_user(token)
        print(user.id)
        print("hi")
        if user:
            return { 'pk': str(user.id)}
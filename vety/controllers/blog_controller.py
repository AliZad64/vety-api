from django.contrib.auth import get_user_model, authenticate
from django.shortcuts import get_object_or_404
from config.utils.permissions import create_token, AuthBearer
from config.utils.schemas import MessageOut
from django.db.models import Q
from ninja import Router
from account.schemas.user_schema import *
blog_controller = Router(tags=["blogs"])
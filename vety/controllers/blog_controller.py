from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import get_object_or_404
from config.utils.permissions import create_token, AuthBearer
from config.utils.schemas import MessageOut
from django.db.models import Q
from ninja import Router, Form
from account.schemas.user_schema import *
from vety.models import Member, Clinic, PetType, Pet
from vety.schemas.pet_schema import *
from vety.schemas.blog_schema import *


User = get_user_model()
blog_controller = Router(tags=["blogs"])

@blog_controller.post('create_blog',auth=AuthBearer(), response= {
    201: BlogOut,
    400: MessageOut
})
def create_blog(request, payload:BlogIn):
    user = get_object_or_404(Clinic, user_id = request.auth['pk'])

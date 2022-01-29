from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import get_object_or_404
from config.utils.permissions import create_token, AuthBearer
from config.utils.schemas import MessageOut
from django.db.models import Q
from ninja import Router, Form
from account.schemas.old_user_schema import *
from vety.models import Member, Clinic, PetType, Pet, RateClinic, Blog, LikeBlog , DislikeBlog
from vety.schemas.pet_schema import *
from vety.schemas.appointment_schema import *
appointment_controller = Router(tags=["appointment"])

@appointment_controller.post("create_appointment", auth=AuthBearer(), response= {
    201: AppointmentSchemaOut,
    400: MessageOut
})
def create_appointment(request, payload:AppointmentSchemaIn):
    return {}

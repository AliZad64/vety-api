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
from vety.models import Member, Clinic, PetType, Pet, RateClinic, Blog, LikeBlog , DislikeBlog, Appointment, Contact
from vety.schemas.pet_schema import *
from vety.schemas.appointment_schema import *
from datetime import datetime,timedelta
from vety.schemas.contact_schema import ContactSchema
contact_controller = Router(tags=["contact"])

@contact_controller.post("contact_us", response= {
    201: MessageOut,
    400: MessageOut
})
def contact_us(request, payload:ContactSchema):
    contact = Contact.objects.create(**payload.dict())
    if contact:
        return 201, {"message": "message has been sent"}
    return 400, {"message":"bad request"}
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
from vety.models import Member, Clinic, PetType, Pet, RateClinic, Blog, LikeBlog , DislikeBlog, Appointment, Contact , Vaccine , Report
from vety.schemas.pet_schema import *
from vety.schemas.appointment_schema import *
from datetime import datetime,timedelta
from vety.schemas.report_schema import *
from vety.schemas.home_schema import HomeSchema
home_controller = Router(tags=["Home_Page"])

@home_controller.get("home_page", response= {
    200: HomeSchema,
    404: MessageOut,
})
def home_page(request):
    clinic = Clinic.objects.order_by('?')[:3]
    blog = Blog.objects.order_by('?')[:3]
    print(clinic)
    print(blog)
    return {
        "clinic": list(clinic),
        "blog": list(blog)
    }

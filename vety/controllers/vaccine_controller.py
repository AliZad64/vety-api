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
from vety.models import Member, Clinic, PetType, Pet, RateClinic, Blog, LikeBlog , DislikeBlog, Appointment, Contact , Vaccine
from vety.schemas.pet_schema import *
from vety.schemas.appointment_schema import *
from datetime import datetime,timedelta
from vety.schemas.vaccine_schema import *

vaccine_controller = Router(tags= ["vaccine"])


@vaccine_controller.get("all_pet_vaccine", auth=AuthBearer(), response = {
    200: List[VaccineOut],
    404: MessageOut
})
def all_pet_vaccine(request, pet_id:UUID4):
    vaccine = Vaccine.objects.filter(pet= pet_id)
    if vaccine:
        return vaccine
    return 404, {"message": "this pet doesn't have any vaccines"}

@vaccine_controller.get("one_pet_vaccine", auth=AuthBearer(), response = {
    200: VaccineOut,
    404: MessageOut
})
def one_pet_vaccine(request, pet_id:UUID4, clinic_id: UUID4):
    vaccine = Vaccine.objects.filter(pet= pet_id, clinic = clinic_id )
    if vaccine:
        return vaccine
    return 404, {"message": "this pet doesn't have any vaccines"}

@vaccine_controller.post("create_vaccine", auth=AuthBearer(),response= {
    201: MessageOut,
    400: MessageOut,
})
def create_vaccine(request, payload: VaccineIn):
    clinic = get_object_or_404(Clinic,user_id = request.auth['pk'])
    pet = get_object_or_404(Pet,id = payload.pet, clinic = clinic)
    vaccine = Vaccine.objects.create(name = payload.name, company= payload.company, next = payload.next,
                                     pet = pet , clinic = clinic)
    if vaccine:
        return 201 , {"message": "success"}
    return 400, {"message": "bad request"}
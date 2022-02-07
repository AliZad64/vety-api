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
from vety.models import Member, Clinic, PetType, Pet, Vaccine, Report
from vety.schemas.pet_schema import *
pet_controller = Router(tags=['pet'])

User = get_user_model()

@pet_controller.get('all_type', response=List[PetTypeSchema])
def all_type(request):
    return PetType.objects.all()

#---------pet CRUD---------
@pet_controller.post('create_pet', auth=AuthBearer(), response= {
    201: SinglePet,
    400: MessageOut
})
def create_pet(request, payload:PetIn):
    member = get_object_or_404(Member, user = request.auth['pk'])
    pet_type = get_object_or_404(PetType, id = payload.type)
    new_pet = Pet.objects.create(**payload.pet_info.dict(), owner= member, type= pet_type)
    if new_pet:
        return 201, new_pet
    return 400, {'message': 'bad request'}

@pet_controller.get('all_pet', auth=AuthBearer(), response={
    200: List[PetNoClinic],
    404: MessageOut,
})
def all_pet(request):
    user = get_object_or_404(User, id = request.auth['pk'])
    if user.account_type == "member":
        return Pet.objects.filter(owner__user_id= request.auth['pk'])
    if user.account_type == "clinic":
        return Pet.objects.filter(clinic__user_id= request.auth['pk'])

@pet_controller.get('one_pet', auth = AuthBearer(), response= {
    200: PetOut,
    404: MessageOut,
})
def one_pet(request, id: UUID4):
    pet = get_object_or_404(Pet, id = id, owner__user_id = request.auth['pk'])
    user = get_object_or_404(User, id = request.auth['pk'])
    if user.account_type == "member":
        vaccine = Vaccine.objects.filter(pet_id = pet.id)
        report = Report.objects.filter(pet_id = pet.id)
        return {
            "pet": pet,
            "vaccine": vaccine,
            "report": report
        }
    if user.account_type == "clinic":
        clinic = get_object_or_404(Clinic, user_id = user.id)
        pet = get_object_or_404(Pet, clinic_id = clinic.id)
        vaccine = Vaccine.objects.filter(pet_id = pet.id, clinic_id= clinic.id)
        report = Report.objects.filter(pet_id = pet.id , clinic_id= clinic.id)
        return {
            "pet": pet,
            "vaccine": vaccine,
            "report": report
        }
@pet_controller.put('update_pet', auth= AuthBearer(), response= {
    200: MessageOut,
    400: MessageOut
})
def update_pet(request, payload: PetUpdate):
    pet_type = get_object_or_404(PetType, id=payload.type)
    pet = Pet.objects.filter(id = payload.pet_id, owner__user_id= request.auth['pk']).update(**payload.pet_info.dict(), type_id= pet_type)
    if pet:
        return 200, {"message": "updated"}
    return 400, {"message":"bad request"}

@pet_controller.post('post_clinic_pet', auth=AuthBearer(), response= {
    201: MessageOut,
    400: MessageOut,
})
def post_clinic_pet(request, id: UUID4, clinic_id: UUID4):
    try:
        pets = get_object_or_404(Pet,id = id , owner__user_id = request.auth['pk'])
        pet = Pet.objects.get(id = id, owner__user_id= request.auth['pk'], clinic= clinic_id)
        return 400, {"message": "pet already at that clinic"}
    except Pet.DoesNotExist:
        clinic = get_object_or_404(Clinic,id = clinic_id)
        pets.clinic.add(clinic)
        return 201 , {'message': 'succeed'}
    return 400, {'message': 'bad request'}

@pet_controller.delete("delete_pet", auth=AuthBearer(), response= {
    200: MessageOut
})
def delete_pet(request, pet_id: UUID4):
    member = get_object_or_404(Member,user_id = request.auth['pk'])
    pet = get_object_or_404(Pet,owner__user_id = request.auth['pk'], id = pet_id)
    pet.delete()
    return {"message": "deleted successfully"}
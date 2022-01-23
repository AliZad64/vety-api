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
from vety.models import Member, Clinic, PetType, Pet
from vety.schemas.pet_schema import *
pet_controller = Router(tags=['pet'])

User = get_user_model()

@pet_controller.get('all_type', response=List[PetTypeSchema])
def all_type(request):
    return PetType.objects.all()

#---------pet CRUD---------
@pet_controller.post('create_pet', auth=AuthBearer(), response= {
    201: PetOut,
    400: MessageOut
})
def create_pet(request, payload:PetIn, type_id:UUID4):
    member = get_object_or_404(Member, user = request.auth['pk'])
    pet_type = get_object_or_404(PetType, id = type_id)
    new_pet = Pet.objects.create(**payload.dict(), owner= member, type_id= pet_type)
    if new_pet:
        return 201, new_pet
    return 400, {'message': 'bad request'}

@pet_controller.get('all_pet', auth=AuthBearer(), response={
    200: List[SinglePet],
    404: MessageOut,
})
def all_pet(request):
    return Pet.objects.filter(owner__user_id= request.auth['pk'])

@pet_controller.get('all_pet2', auth=AuthBearer(), response={
    200: List[SinglePet],
    404: MessageOut,
})
@pet_controller.get('one_pet', auth = AuthBearer(), response= {
    200: SinglePet,
    404: MessageOut,
})
def one_pet(request, id: UUID4):
    return get_object_or_404(Pet, id = id, owner__user_id = request.auth['pk'])

@pet_controller.put('update_pet', auth= AuthBearer(), response= {
    203: MessageOut,
    400: MessageOut
})
def update_pet(request, payload: PetIn, type_id: UUID4, id: UUID4):
    pet = Pet.objects.filter(id = id, owner__user_id= request.auth['pk']).update(**payload.dict(), type_id= type_id)
    if pet:
        return 203, {"message": "updated"}
    return 400, {"message":"bad request"}

@pet_controller.post('post_clinic_pet', auth=AuthBearer(), response= {
    201: MessageOut,
    400: MessageOut,
})
def post_clinic_pet(request, id: UUID4, payload: PetInClinic):
    try:
        pets = get_object_or_404(Pet,id = id , owner__user_id = request.auth['pk'])
        pet = Pet.objects.get(id = id, owner__user_id= request.auth['pk'], clinic_id= payload.clinic_id)
    except Pet.DoesNotExist:
        clinic = get_object_or_404(Clinic,id = payload.clinic_id)
        pets.clinic_id.add(clinic)
        return 201 , {'message': 'succeed'}
    return 400, {'message': 'bad request'}
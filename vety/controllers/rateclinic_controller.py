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
from vety.models import Member, Clinic, PetType, Pet, RateClinic
from vety.schemas.pet_schema import *
from vety.schemas.rateclinic_schema import *
clinic_rating_controller = Router(tags=["clinic_rating"])

@clinic_rating_controller.post('rate_clinic',auth=AuthBearer(), response= {
    201: MessageOut,
    400: MessageOut
})
def rate_clinic(request, payload:RateClinicSchemaIn):
    user = get_object_or_404(Member,user_id = request.auth['pk'])
    clinic = get_object_or_404(Clinic, id = payload.clinic)
    try:
        rating = RateClinic.objects.get(member = user, clinic = clinic, point = payload.point)
        return 400, {"message": "user already rated the clinic with that number"}
    except:
        try:
            rating = RateClinic.objects.get(member= user, clinic = clinic)
            rating.objects.update(member = user, clinic= clinic,point = payload.point)
            return 201, {"message": "updated your rating successfully"}
        except:
            rating = RateClinic.objects.create(member = user , clinic= clinic, point = payload.point)
            return 201, {"message": "your rating has been saved"}

@clinic_rating_controller.get("one_clinic_rate",auth=AuthBearer(), response= {
    200: RateClinicSchemaOut
})
def one_clinic_rate(request, clinic_id: UUID4):
    return get_object_or_404(RateClinic, member__user_id = request.auth['pk'], clinic = clinic_id )

@clinic_rating_controller.delete("delete_clinic_rate", auth=AuthBearer(), response= {
    201: MessageOut
})
def delete_clinic_rate(request, clinic_id: UUID4):
    rating = get_object_or_404(RateClinic,member__user_id = request.auth['pk'], clinic = clinic_id )
    rating.delete()
    return 201, {"message": "deleted successfully "}
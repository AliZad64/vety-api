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
from vety.models import Member, Clinic, PetType, Pet, RateClinic, Blog, LikeBlog , DislikeBlog, Appointment
from vety.schemas.pet_schema import *
from vety.schemas.appointment_schema import *
from datetime import datetime,timedelta , date
appointment_controller = Router(tags=["appointment"])

@appointment_controller.post("create_appointment", auth=AuthBearer(), response= {
    201: AppointmentSchemaOut,
    400: MessageOut
})
def create_appointment(request, payload:AppointmentSchemaIn):
    #get the date without seconds
    start_date = payload.start_date.replace(minute=00).strftime('%Y-%m-%d %H:%M')
    #get the time only for validate
    start_time = payload.start_date.strftime("%H:%M")
    end_date_update = payload.start_date.replace(minute= 00) + timedelta(hours=1)
    end_date = end_date_update.strftime('%Y-%m-%d %H:%M')
    end_time = end_date_update.strftime("%H:%M")
    print(start_time)
    print(end_time)
    member = get_object_or_404(Member, user_id = request.auth['pk'])
    clinic = get_object_or_404(Clinic, id = payload.clinic)

    #check if clinic is available at these times
    clinic_check = Clinic.objects.filter(start_date__lte = start_time , end_date__gte= end_time, id = payload.clinic)
    if not clinic_check:
        return 400 , {"message": "that time is not available for that clinic"}

    #check if clinic is available at this date
    clinic_date_check = Clinic.objects.filter(clinicss_appointment__start_date__exact= start_date, id = payload.clinic)
    if clinic_date_check:
        return 400, {"message": "this date is already booked"}

    #check if member haven't booked an appointment at this date
    member_date_check = Member.objects.filter(user_id = request.auth['pk'], memberss_appointment__start_date__exact= start_date)
    if member_date_check:
        return 400, {"message": "you already have booked at this date to a clinic"}

    x = Appointment.objects.create(clinic = clinic, member = member, start_date= start_date, end_date= end_date)
    if x:
        return 201, x
    return 400, {"message": "bad request"}

@appointment_controller.get('get_all_appointment',auth = AuthBearer(), response={
    200: List[AppointmentSchemaOut],
    400: MessageOut
})
def get_all_appointment(request ):
    return Appointment.objects.filter(member__user_id= request.auth['pk'])

@appointment_controller.get('get_all_clinic_related_appointment', auth = AuthBearer(), response={
    200: List[AppointmentSchemaOut],
    400: MessageOut
})
def get_all_clinic_related_appointment(request , clinic_id: UUID4):
    return Appointment.objects.filter(member__user_id= request.auth['pk'], clinic_id = clinic_id )

@appointment_controller.get('get_one_appointment', auth = AuthBearer(), response={
    200: AppointmentSchemaOut,
    400: MessageOut
})
def get_one_appointment(request , appointment_id: UUID4):
    return get_object_or_404(Appointment,member__user_id= request.auth['pk'], id = appointment_id )

@appointment_controller.delete('delete_appointment', auth = AuthBearer(), response={
    200: MessageOut,
    400: MessageOut
})
def delete_appointment(request , appointment_id: UUID4):
    appointment = get_object_or_404(Appointment,member__user_id= request.auth['pk'], id = appointment_id )
    appointment.delete()
    return 200, {"message": "deleted successfully"}
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

report_controller = Router(tags= ["report"])
report_clinic_controller = Router(tags= ["report_clinic"])

@report_controller.get("all_pet_report", auth=AuthBearer(), response= {
    200: List[ReportOut],
    404: MessageOut,
})
def all_report(request, pet_id: UUID4):
    member = get_object_or_404(Member, user_id = request.auth['pk'])
    report = Report.objects.filter(pet_id = pet_id)
    if report:
        return report
    return 404, {"message": "this pet doesn't have any reports"}

@report_controller.get("one_pet_report", auth=AuthBearer(), response={
    200: ReportOut,
    404: MessageOut
})
def one_pet_report(request, report_id: UUID4):
    user = get_object_or_404(Member, user_id=request.auth['pk'])
    report = Report.objects.get(id=report_id)
    if report:
        return report
    return 404, {"message": "this pet doesn't have any reports"}

@report_clinic_controller.get("all_clinic_report", auth = AuthBearer(), response= {
    200: List[ReportClinicOut],
    404: MessageOut
})
def all_clinic_report(request):
    clinic = get_object_or_404(Clinic, user_id = request.auth['pk'])
    report = Report.objects.filter(clinic = clinic)
    if report:
        return report
    return 404, {"message": "clinic doesn't have reports"}

@report_clinic_controller.get("one_clinic_report", auth=AuthBearer(), response= {
    200: ReportClinicOut,
    404: MessageOut
})
def one_clinic_report(request, report_id: UUID4):
    clinic = get_object_or_404(Clinic, user_id=request.auth['pk'])
    pet = get_object_or_404(Pet, clinic=clinic)
    report = get_object_or_404(Report, clinic=clinic, id=report_id)
    if report:
        return report
    return 404, {"message": "clinic don't have report with that pet "}

@report_clinic_controller.post("create_report", auth=AuthBearer(), response= {
    201: ReportClinicOut,
    404: MessageOut,
})
def create_report(request, payload:ReportIn):
    clinic = get_object_or_404(Clinic,user_id = request.auth['pk'])
    pet = get_object_or_404(Pet,id = payload.pet, clinic = clinic)
    report = Report.objects.create(title = payload.title, allergy= payload.allergy, description = payload.description,
                                     pet = pet , clinic = clinic)
    if report:
        return 201 , report
    return 400, {"message": "bad request"}

@report_clinic_controller.put("update_report", auth=AuthBearer(), response= {
    201: ReportClinicOut,
    404: MessageOut,
})
def update_report(request, payload:ReportUpdate):
    clinic = get_object_or_404(Clinic, user_id = request.auth['pk'])
    report = Report.objects.filter(id = payload.report_id, clinic = clinic)
    if report:
        report.update(**payload.report_update.dict())
        report = Report.objects.get(id = payload.report_id)
        return 201, report
    return 404, {"message": "report not foundS"}

@report_clinic_controller.delete("delete_report", auth=AuthBearer(), response= {
    200: MessageOut,
    404: MessageOut,
})
def delete_report(request, report_id: UUID4):
    clinic = get_object_or_404(Clinic, user_id=request.auth['pk'])
    report = Report.objects.filter(id=report_id, clinic=clinic)
    if report:
        report.delete()
        return 200, {"message": "report has been deleted"}
    return 404, {"message: report not found"}
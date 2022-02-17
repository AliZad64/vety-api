from account.schemas.user_schema import SignUpOut, ClinicSchema, MemberSchema
from pydantic import UUID4, ValidationError, validator
from typing import List
from datetime import date , datetime
from ninja.orm import create_schema
from pydantic import Field
from ninja.files import UploadedFile

from ninja import  Schema , File
from ninja.orm import create_schema

from pydantic import EmailStr
from config.utils.schemas import Entity
from config.utils.schemas import Token
from account.models import EmailAccount
from vety.models import Member
from vety.schemas.pet_schema import PetNoClinic

class ReportSchema(Schema):
    title: str
    allergy: str
    description: str

class ReportIn(ReportSchema):
    pet: UUID4

class ReportUpdate(Schema):
    report_update: ReportIn
    report_id: UUID4

class ReportOut(Entity, ReportSchema):
    clinic: ClinicSchema
    created: datetime = None
    updated: datetime = None
class ReportClinicOut(Entity,ReportSchema):
    pet: PetNoClinic
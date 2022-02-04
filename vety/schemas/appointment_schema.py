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

def convert_datetime_to_iso_8601_with_z_suffix(dt: datetime) -> str:
    return dt.strftime('%Y-%m-%d %H:%M')
class AppointmentSchema(Schema):
    start_date: datetime
    class Config:
        json_encoders = {
            datetime: convert_datetime_to_iso_8601_with_z_suffix
        }

class AppointmentSchemaIn(AppointmentSchema):
    clinic: UUID4


class AppointmentSchemaOut(Entity, AppointmentSchema):
    end_date: datetime
    clinic: ClinicSchema


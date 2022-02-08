from account.schemas.user_schema import SignUpOut, MemberSchema, ClinicSchema
from pydantic import UUID4
from typing import List
from datetime import date
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
from vety.schemas.pet_schema import testMemberOut

class RateClinicSchema(Schema):
    point: int

class RateClinicSchemaOut(RateClinicSchema, Entity):
    pass
class RateClinicSchemaIn(RateClinicSchema):
    clinic: UUID4


    
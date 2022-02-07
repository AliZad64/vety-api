from account.schemas.user_schema import SignUpOut, ClinicSchema, MemberSchema
from pydantic import UUID4
from typing import List
from datetime import date, datetime
from ninja.orm import create_schema
from pydantic import Field
from ninja.files import UploadedFile

from ninja import  Schema , File
from ninja.orm import create_schema

from pydantic import EmailStr, validator
from config.utils.schemas import Entity
from config.utils.schemas import Token
from account.models import EmailAccount
from vety.models import Member
#-----for testing and they are not used anymore
class testMemberOut(Schema):
    user: SignUpOut
    gender:str = None
    birth: date = None

class testClinicOut(Schema):
    user: SignUpOut
    facebook: str = None
    instagram: str = None
    work_range: str = None


#for vaccine and report schemas
class NameClinicSchema(Entity):
    clinic_name: str = None
class VaccineSchema(Entity):
    name: str
    clinic: NameClinicSchema
    created: datetime = None


class ReportSchema(Entity):
    title: str
    clinic: NameClinicSchema
    description: str = None
    created: datetime = None

class PetTypeSchema(Entity):
    name: str

class PetSchema(Schema):
    name: str
    gender: str = None
    image: str = None
    family: str = None
    weight: int = None
    adopt_date: date = None
    age: int = None

    @validator('gender')
    def right_gender(cls, v):
        if v:
            if v != "male" and v != "female":
                raise ValueError("choose the right gender either male or female")
        return v
    @validator('weight')
    def right_weight(cls,v):
        if v:
            if v <= 0:
                raise ValueError("put real weight")
        return v

class SinglePet(PetSchema, Entity):
    type: PetTypeSchema
    clinic: List[ClinicSchema]

class PetOut(Schema):
    pet: SinglePet
    vaccine: VaccineSchema
    report: ReportSchema
#this is for all pets endpoint so we don't show the clinics for each pet
class PetNoClinic(PetSchema, Entity):
    type: PetTypeSchema = None
class PetIn(Schema):
    pet_info: PetSchema
    type: UUID4

class PetUpdate(PetIn):
    pet_id: UUID4
#this is for user output
class PetUserOut(PetSchema,Entity):
    pass

class PetInClinic(Schema):
    pet: UUID4
    clinic: UUID4


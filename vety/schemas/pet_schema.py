from account.schemas.old_user_schema import SignUpOut
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


class testMemberOut(Schema):
    user: SignUpOut
    gender:str = None
    birth: date = None

class testClinicOut(Schema):
    user: SignUpOut
    facebook: str = None
    instagram: str = None
    work_range: str = None

class PetTypeSchema(Entity):
    name: str

class PetSchema(Schema):
    name: str
    image: str = None
    family: str = None
    weight: int = None
    birth: date = None
    age: int = None


class SinglePet(PetSchema, Entity):
    type_id: PetTypeSchema
    clinic: List[testClinicOut]

class PetOut(SinglePet):
    owner: testMemberOut
    clinic: List[testClinicOut]

class PetIn(PetSchema):
    pass
#this is for user output
class PetUserOut(PetSchema,Entity):
    pass
class PetInClinic(Schema):
    clinic_id: UUID4


from turtle import st
from typing import List
from datetime import date
from ninja.orm import create_schema
from pydantic import Field
from ninja.files import UploadedFile

from ninja import  Schema , File
from ninja.orm import create_schema
from pydantic import UUID4
from pydantic import EmailStr
from config.utils.schemas import Entity
from config.utils.schemas import Token
from account.models import EmailAccount
from vety.models import Member, Pet

#----- for pet schema-----

# ----------city schema---------
class CityOut(Entity):
    name: str = None

#------user sign up schema----------
class SignUp(Schema):
    first_name: str
    last_name: str
    email: str = None
    password1: str
    password2: str
    phone_number: str

class SignUpIn(SignUp):
    pass

class SignUpOut(Entity):
    first_name: str
    last_name: str
    email: EmailStr = None
    phone_number: str
    city: CityOut = None
    area: str = None
    account_type: str
    user_image: str = None
    deleted_at: bool = None



#------user signin-----

class SigninIn(Schema):
    email: str = None
    phone_number: str = None
    password: str

class SigninOut(SignUpOut):
    pass
#---------user CLININC account--------

class ClinicSchema(Schema):
    id: UUID4
    facebook: str
    instagram: str
    work_range: str

class SignOutClinic(SigninOut):
    clinic: ClinicSchema = Field(None, alias= 'clinicss')

class ClinicInfo(ClinicSchema):
    user: SigninOut

class ClinicOut(Schema):
    profile: SignOutClinic
    token: Token

#------- user MEMBER account------
class PetUserOut(Entity):
    name: str
    image: str = None
    family: str = None
    weight: int = None
    birth: date = None
    age: int = None
    clinic: List[ClinicInfo] = Field(None, alias= 'pet_clinic')

class MemberSchema(Schema):
    gender:str = None
    birth: date = None
    pet: List[PetUserOut] = Field(None, alias= "owner_pet")

class SignInOutMember(SigninOut):
    member: MemberSchema = Field(None, alias= 'memberss')

class MemberOut(Schema):
    profile: SignInOutMember
    token: Token


#------update Member account------
class UserUpdate(Schema):
    first_name: str = None
    last_name: str = None
    area: str = None
    user_image: str = None
class MemberUpdate(MemberSchema):
    pass

class MemberUpdateIn(Schema):
    user: UserUpdate = None
    member: MemberUpdate = None

class MemberUpdateOut(SignInOutMember):
    pass



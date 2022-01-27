import re
from turtle import st
from typing import List
from datetime import date, time
from ninja.orm import create_schema
from pydantic import Field, BaseModel, ValidationError, validator
from ninja.files import UploadedFile
from django.core.validators import validate_email
from ninja import  Schema , File
from ninja.orm import create_schema
from pydantic import UUID4
from pydantic import EmailStr
from config.utils.schemas import Entity
from config.utils.schemas import Token
from account.models import EmailAccount
from vety.models import Member, Pet



# ----------city schema---------
class CityOut(Schema):
    name: str = None
class ZoneOut(Schema):
    name: str = None
class AddressOut(Entity):
    city: CityOut
    zone: ZoneOut = None
#------user sign up schema----------
class SignUp(Schema):
    first_name: str
    last_name: str
    email: str = None
    password1: str = Field(min_length=8)
    password2: str = Field(min_length=8)
    phone_number: str = Field(min_length=11, max_length=15 , regex=r'^07([\s\d]+)$')

class SignUpIn(SignUp):
    pass

class SignUpOut(Entity):
    first_name: str
    last_name: str
    email: EmailStr = None
    phone_number: str
    address: AddressOut = None
    area: str = None
    account_type: str
    user_image: str = None
    deleted_at: bool = None



#------user signin-----

class SigninIn(Schema, BaseModel):
    user: str
    password: str = Field(min_length=8)




class SigninOut(SignUpOut):
    pass
#---------user CLININC account--------

class ClinicSchema(Entity):
    user: SigninOut
    facebook: str
    instagram: str
    start_date: time = None
    end_date: time = None
    rating_average: int = None


class ClinicInfo(ClinicSchema):
    user: SigninOut

class ClinicOut(Schema):
    profile: ClinicSchema
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
    user: SigninOut
    gender:str = None
    birth: date = None
    pet: List[PetUserOut] = Field(None, alias= "pet_owner")

class MemberNoPetSchema(Schema):
    user: SigninOut
    gender:str = None
    birth: date = None

class MemberOut(Schema):
    profile: MemberSchema
    token: Token


#------update Member account------
class UserUpdate(Schema):
    first_name: str = None
    last_name: str = None
    address: UUID4 = None
    user_image: str = None
class MemberUpdate(Schema):
    gender: str = None
    birth: date = None

    @validator('gender')
    def right_gender(cls,v):
        if v:
            if v  != "male" and v != "female":
                raise ValueError("choose the right gender")
        return v
class MemberUpdateIn(Schema):
    user: UserUpdate = None
    member: MemberUpdate = None

class MemberUpdateOut(MemberSchema):
    pass



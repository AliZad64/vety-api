from typing import List
from datetime import date
from ninja.orm import create_schema
from pydantic import Field

from ninja import  Schema
from ninja.orm import create_schema
from pydantic import UUID4
from pydantic import EmailStr
from config.utils.schemas import Entity
from config.utils.schemas import Token
from account.models import EmailAccount
from vety.models import Member
# ----------city schema---------
class CityOut(Entity):
    name: str = None

#------user sign up schema----------
class SignUp(Schema):
    first_name: str
    last_name: str
    email: EmailStr
    password1: str
    password2: str
    phone_number: str = None

class SignUpIn(SignUp):
    pass

class SignUpOut(Entity):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str = None
    city: CityOut = None
    area: str = None
    account_type: str
    user_image: str = None
    deleted_at: bool = None



#------user signin-----

class SigninIn(Schema):
    email: EmailStr = None
    phone_number: str = None
    password: str
    
    
#------- user MEMBER account------

class MemberSchema(Schema):
    gender:str = None
    birth: date = None

class SignInOut(SignUpOut):
    member: MemberSchema = Field(None, alias= 'memberss')
    
class MemberOut(Schema):
    profile: SignInOut
    token: Token



#------update Member account------
class UserUpdate(Schema):
    first_name: str = None
    last_name: str = None
    area: str = None
    user_image: str = Field(...)
class MemberUpdate(Schema):
    gender: str = None
class MemberUpdateIn(Schema):
    user: UserUpdate = None
    member: MemberUpdate = None




MemberSchema = create_schema(Member, depth = 2)
UserSchema = create_schema(EmailAccount)
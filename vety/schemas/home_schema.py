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
from vety.schemas.pet_schema import PetUserOut
from vety.schemas.blog_schema import BlogOut
class HomeSchema(Schema):
    clinic: List[ClinicSchema]
    blog: List[BlogOut]
from account.schemas.old_user_schema import *
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
from vety.schemas.pet_schema import *

class BlogSchema(Schema):
    title: str
    description: str
    image: str = None

class BlogIn(BlogSchema):
    type_id: UUID4

class BlogOut(BlogSchema):
    owner: testClinicOut
    type_id: PetTypeSchema

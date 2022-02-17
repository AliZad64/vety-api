from account.schemas.user_schema import *
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

class AllBlogOut(Entity, BlogSchema):
    owner: ClinicBlogSchemaOut
    type: PetTypeSchema
    like_count: int = None
    dislike_count: int = None
    created: datetime = None
class BlogOut(Entity, BlogSchema):
    owner: ClinicSignOut
    type: PetTypeSchema
    like_count: int = None
    dislike_count: int = None
    created: datetime = None

class UserBlogOut(BlogOut):
    is_like: bool = None
    is_dislike: bool = None

class BlogUpdate(BlogSchema):
    title: str = None
    description :str = None
    image: str = None
    type_id: UUID4 = None

class BlogSortById(Schema):
    type: UUID4

class BlogNoOwner(Entity,BlogSchema):
    type: PetTypeSchema
    like_count: int = None
    dislike_count: int = None

class ClinicBlogs(ClinicSchema):
    blog: BlogNoOwner = Field(None, alias="fromClinic")
from account.schemas.user_schema import SignUpOut
from pydantic import UUID4
from typing import List
from datetime import date
from ninja.orm import create_schema
from pydantic import Field
from ninja.files import UploadedFile
from account.schemas.user_schema import ClinicInfo
from ninja import  Schema , File
from ninja.orm import create_schema
from pydantic import EmailStr
from config.utils.schemas import Entity
from config.utils.schemas import Token
from account.models import EmailAccount
from vety.models import Member
from vety.schemas.pet_schema import testMemberOut

class LikeSchema(Schema):
    is_like: bool

class LikeSchemaIn(Schema):
    blog: UUID4

class DislikeSchema(Schema):
    is_dislike: bool

class DislikeSchemaIn(Schema):
    blog: UUID4

class BlogRatingSchema(Schema):
    like: LikeSchema = None
    dislike: DislikeSchema = None

class CheckRateBlogSchema(Schema):
    is_like: bool = None
    is_dislike: bool = None
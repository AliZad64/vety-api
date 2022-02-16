from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import get_object_or_404
from config.utils.permissions import create_token, AuthBearer
from config.utils.schemas import MessageOut
from django.db.models import Q
from ninja import Router, Form
from account.schemas.old_user_schema import *
from vety.models import Member, Clinic, PetType, Pet, Blog
from vety.schemas.pet_schema import *
from vety.schemas.blog_schema import *


User = get_user_model()
blog_controller = Router(tags=["blogs"])

@blog_controller.post('create_blog',auth=AuthBearer(), response= {
    201: BlogOut,
    400: MessageOut
})
def create_blog(request, payload:BlogIn):
    user = get_object_or_404(Clinic, user_id = request.auth['pk'])
    type = get_object_or_404(PetType, id = payload.type_id)
    blog = Blog.objects.create(title= payload.title , description=payload.description, image=payload.image,
                               type= type, owner= user)
    if blog:
        return 201 , BlogOut
    return 400, {"message": "bad request"}

@blog_controller.get("all_blog", response=List[AllBlogOut])
def all_blog(request):
    return Blog.objects.all()

@blog_controller.get("filter_by_clinic", response= {
    200: List[BlogOut],
    404: MessageOut,
})
def filter_by_clinic(request, clinic_id: UUID4):
    blog = Blog.objects.filter(clinic_id = clinic_id)
    if blog:
        return blog
    return 404, {"messag": "clinic not found or clinic does not have blogs"}
@blog_controller.get("one_blog", response=BlogOut)
def one_blog(request, id:UUID4):
    return get_object_or_404(Blog, id = id)

@blog_controller.delete("delete_blog", auth=AuthBearer(), response= {
    200: MessageOut,
    400: MessageOut
})
def delete_blog(request, id: UUID4):
    user = get_object_or_404(User, id = request.auth['pk'])
    blog = get_object_or_404(Blog, id=id ,owner= user, )
    blog.delete()
    return 200, {"message": "deleted successfully"}

@blog_controller.get("filter_by_type", response= List[BlogOut])
def filter_by_type(request, id: UUID4):
    return Blog.objects.filter(type = id)

@blog_controller.get("all_clinic_blog",auth=AuthBearer(), response= {
    200: ClinicBlogs,
    404: MessageOut,
})
def all_clinic_blog(request):
    clinic = get_object_or_404(Clinic, user_id = request.auth['pk'])
    return clinic
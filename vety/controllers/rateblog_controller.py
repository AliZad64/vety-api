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
from vety.models import Member, Clinic, PetType, Pet, RateClinic, Blog, LikeBlog , DislikeBlog
from vety.schemas.pet_schema import *
from vety.schemas.rateblog_schema import *
blog_rating_controller = Router(tags=["blog_rating"])

@blog_rating_controller.post("like_blog", auth=AuthBearer(), response= {
    201: MessageOut,
    200: MessageOut,
    400: MessageOut,
})
def like_blog(request, blog_id: UUID4 ):
    user = get_object_or_404(Member, user_id = request.auth['pk'])
    blog = get_object_or_404(Blog, id = blog_id)
    try:
        like = LikeBlog.objects.get(member = user , blog = blog, is_like= True)
        like.delete()
        return 201, {"message": "like removed successfully"}
    except:
        dislike = DislikeBlog.objects.filter(member = user , blog = blog, is_dislike= True)
        if dislike:
            dislike.delete()
        like = LikeBlog.objects.create(member=user , blog = blog , is_like= True)
        if like:
            return 201, {"message": "liked the blog successfully"}


@blog_rating_controller.post("dislike_blog", auth=AuthBearer(), response= {
    201: MessageOut,
    200: MessageOut,
    400: MessageOut,
})
def dislike_blog(request, blog_id: UUID4):
    user = get_object_or_404(Member, user_id = request.auth['pk'])
    blog = get_object_or_404(Blog, id = blog_id)
    try:
        dislike = DislikeBlog.objects.get(member = user , blog = blog, is_dislike= True)
        dislike.delete()
        return 201, {"message": "dislike removed successfully"}
    except:
        like = LikeBlog.objects.filter(member = user , blog = blog, is_like= True)
        if like:
            like.delete()
        dislike = DislikeBlog.objects.create(member=user , blog = blog , is_dislike= True)
        if dislike:
            return 201, {"message": "disliked the blog"}

@blog_rating_controller.get("check_like_dislike", auth=AuthBearer(), response= {
    200: CheckRateBlogSchema,
    404: MessageOut
})
def check_like_dislike(request, blog_id:UUID4):
    member = get_object_or_404(Member, user_id = request.auth['pk'])
    blog = get_object_or_404(Blog, id = blog_id)
    dislike = DislikeBlog.objects.filter(blog=blog, member=member)
    like = LikeBlog.objects.filter(blog=blog, member=member)
    if like and dislike:
        dislike = DislikeBlog.objects.get(blog = blog , member = member)
        like = LikeBlog.objects.get(blog = blog , member = member)
        return {
            "is_like": like.is_like,
            "is_dislike": dislike.is_dislike
        }
    if like:
        like = LikeBlog.objects.get(blog=blog, member=member)
        return {
            "is_like": like.is_like,
            "is_dislike": False
        }
    if dislike:
        dislike = DislikeBlog.objects.get(blog = blog , member = member)
        return {
            "is_like": False,
            "is_dislike": dislike.is_dislike
        }
    return 404, {"message": "this user hasn't liked nor disliked this blog"}
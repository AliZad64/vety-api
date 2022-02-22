from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from config.utils.permissions import create_token, AuthBearer
from config.utils.schemas import MessageOut
from django.db.models import Q
from ninja import Router, Form
from account.schemas.user_schema import *
from vety.models import Member, Clinic, RateClinic
from account.models import Address
from email_validator import validate_email, EmailNotValidError

account_controller = Router(tags=["auth"])
address_controller = Router(tags=["address"])
clinic_controller = Router(tags=["clinic"])

User = get_user_model()


# related to the project
@account_controller.post('signup', response={
    400: MessageOut,
    201: MemberOut,
})
def signup(request, account_in: SignUpIn):
    if account_in.password1 != account_in.password2:
        return 400, {'detail': 'Passwords do not match!'}

    # validate email
    if account_in.email:
        try:
            validate_email(account_in.email)
        except EmailNotValidError:
            return 400, {'message': 'invalid email'}
        except ValidationError:
            return 400, {'message': 'invalid email'}

    try:
        User.objects.get(Q(email=account_in.email) | Q(phone_number=account_in.phone_number))
    except User.DoesNotExist:
        new_user = User.objects.create_user(
            first_name=account_in.first_name,
            last_name=account_in.last_name,
            phone_number=account_in.phone_number,
            email=account_in.email,
            password=account_in.password1
        )

        member = Member.objects.create(user=new_user)
        token = create_token(member.user)
        return 201, {
            'profile': member,
            'token': token,
        }

    return 400, {'message': 'User already registered!'}


@account_controller.post('sign_in', response={
    200: testUserOut,
    404: MessageOut,
    400: MessageOut,
})
def sign_in(request, signin_in: SigninIn):
    # sign in by phone number
    if not signin_in.user:
        return 404, {'message': 'enter number or email'}
    user = authenticate(phone_number=signin_in.user, password=signin_in.password)
    if not user:
        # validate email
        try:
            validate_email(signin_in.user)
        except EmailNotValidError:
            return 400, {'message': 'user does not exist'}
        except ValidationError as e:
            return 400, {'message': 'user does not exist'}

        # sign in by email
        user = get_object_or_404(User, email=signin_in.user)
        if not check_password(signin_in.password, user.password):
            return 404, {'message': 'wrong password'}
    token = create_token(user)
    login = get_object_or_404(User, id = user.id)
    return 200, {
        'profile': login,
        'token': token,
    }


@account_controller.get('me', auth=AuthBearer(), response={
    200: testUserSchemaOut
})
def me(request):
    user =  get_object_or_404(User, id=request.auth['pk'])
    return user

@account_controller.put('update_account', auth=AuthBearer(), response={
    200: MemberUpdateOut,

})
def update_account(request, update_in: MemberUpdateIn):
    User.objects.filter(id=request.auth['pk']).update(**update_in.user.dict())
    Member.objects.filter(user=request.auth['pk']).update(**update_in.member.dict())
    # .update(gender = update_in.gender)
    return get_object_or_404(Member, user_id=request.auth['pk'])

@account_controller.post('update_account_form', deprecated=True, auth=AuthBearer(), response={
    200: MemberUpdateOut,

})
def update_account_form(request, update_in: MemberUpdateForm = Form(...) , user_image: UploadedFile = File(...)):
    User.objects.filter(id=request.auth['pk']).update(**update_in.user.dict(), user_image = user_image)
    Member.objects.filter(user=request.auth['pk']).update(**update_in.member.dict())
    # .update(gender = update_in.gender)
    return get_object_or_404(Member, user_id=request.auth['pk'])

@account_controller.delete("delete_account", auth=AuthBearer(),response= {
    200: MessageOut,
})
def delete_account(request):
    member = get_object_or_404(Member, user_id = request.auth['pk'])
    user = User.objects.filter(id = request.auth['pk'])
    user.delete()
    return 200,{"message":"deleted"}
@clinic_controller.post('Clinic_Sign_in', deprecated = True, response={
    200: ClinicOut,
    404: MessageOut,
    400: MessageOut,
    403:MessageOut,
})
def clinic_sign_in(request, signin_in: SigninIn):
    # sign in by phone number
    if not signin_in.user:
        return 404, {'message': 'User does not exist'}

    user = authenticate(phone_number=signin_in.user, password=signin_in.password)
    if not user:
        # validate email
        try:
            validate_email(signin_in.user)
        except EmailNotValidError:
            return 400, {'message': 'invalid email'}
        except ValidationError:
            return 400, {'message': 'invalid email'}

        # sign in by email
        user = get_object_or_404(User, email=signin_in.user)
        if not check_password(signin_in.password, user.password):
            return 404, {'message': 'wrong password'}
    token = create_token(user)
    if user.account_type == "clinic":
        return {
            'profile': get_object_or_404(Clinic, user = user),
            'token': token,
        }
    return 403, {"message": "invalid clinic account"}


@clinic_controller.get('all_clinics', response={
    200: List[ClinicSchema]
})
def all_clinic(request):
    return Clinic.objects.all().exclude(clinic_name = "vety")


@clinic_controller.get('one_clinics', response={
    200: ClinicFullInfoAndRating
})
def one_clinic(request, id: UUID4):
    clinic = get_object_or_404(Clinic, id= id)
    try:
        rating = RateClinic.objects.get(member__user_id = request.auth['pk'], clinic = clinic )
        clinic.user_rating = rating.point
        return clinic
    except:
        return clinic
@address_controller.get('all_address',response={
    200: List[AddressOut]
})
def all_address(request):
    return Address.objects.all()


# @account_controller.post('change-password', auth=AuthBearer(), response={
#     200: MessageOut,
#     400: MessageOut
# })
# def change_password(request, password_update_in: ChangePasswordSchema):
#     # user = authenticate(get_object_or_404(User, id=request.auth['pk']).email, password_update_in.old_password)
#     if password_update_in.new_password1 != password_update_in.new_password2:
#         return 400, {'detail': 'passwords do not match'}
#     user = get_object_or_404(User, id=request.auth['pk'])
#     is_it_him = user.check_password(password_update_in.old_password)

#     if not is_it_him:
#         return 400, {'detail': 'Dude, make sure you are him!'}

#     user.set_password(password_update_in.new_password1)
#     user.save()
#     return {'detail': 'password updated successfully'}

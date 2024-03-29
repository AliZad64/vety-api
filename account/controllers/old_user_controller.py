# from django.contrib.auth import get_user_model, authenticate
# from django.contrib.auth.hashers import check_password
# from django.core.exceptions import ValidationError
# from django.core.validators import validate_email
# from django.shortcuts import get_object_or_404
# from config.utils.permissions import create_token, AuthBearer
# from config.utils.schemas import MessageOut
# from django.db.models import Q
# from ninja import Router, Form
# from account.schemas.old_user_schema import *
# from vety.models import Member, Clinic
#
# account_controller = Router(tags=["auth"])
# clinic_controller = Router(tags=["clinic"])
#
# User = get_user_model()
#
#
# # related to the project
# @account_controller.post('signup', response={
#     400: MessageOut,
#     201: MemberOut,
# })
# def signup(request, account_in: SignUpIn):
#     if account_in.password1 != account_in.password2:
#         return 400, {'detail': 'Passwords do not match!'}
#
#     # validate email
#     if account_in.email:
#         try:
#             validate_email(account_in.email)
#         except ValidationError:
#             return 400, {'message': 'invalid email'}
#
#     try:
#         User.objects.get(Q(email=account_in.email) | Q(phone_number=account_in.phone_number))
#     except User.DoesNotExist:
#         new_user = User.objects.create_user(
#             first_name=account_in.first_name,
#             last_name=account_in.last_name,
#             phone_number=account_in.phone_number,
#             email=account_in.email,
#             password=account_in.password1
#         )
#
#         member = Member.objects.create(user=new_user, gender="male")
#         token = create_token(new_user)
#
#         print(member)
#         return 201, {
#             'profile': new_user,
#             'token': token,
#         }
#
#     return 400, {'message': 'User already registered!'}
#
#
# @account_controller.post('signin', response={
#     200: MemberOut,
#     404: MessageOut,
#     400: MessageOut,
# })
# def signin(request, signin_in: SigninIn):
#     # sign in by phone number
#     user = authenticate(phone_number=signin_in.phone_number, password=signin_in.password)
#     if not user:
#         if not signin_in.email:
#             return 404, {'message': 'User does not exist'}
#
#         # validate email
#         try:
#             validate_email(signin_in.email)
#         except ValidationError:
#             return 400, {'message': 'invalid email'}
#
#         # sign in by email
#         user = get_object_or_404(User, email=signin_in.email)
#         if not check_password(signin_in.password, user.password):
#             return 404, {'message': 'wrong password'}
#     token = create_token(user)
#     if user.account_type == "member":
#         return {
#             'profile': user,
#             'token': token,
#         }
#
#
# @account_controller.get('', auth=AuthBearer(), response=SignInOutMember)
# def me(request):
#     print(request.auth['pk'])
#     return get_object_or_404(User, id=request.auth['pk'])
#
#
# @account_controller.put('', auth=AuthBearer(), response={
#     200: MemberUpdateOut,
#
# })
# def update_account(request, update_in: MemberUpdateIn):
#     User.objects.filter(id=request.auth['pk']).update(**update_in.user.dict())
#     Member.objects.filter(user=request.auth['pk']).update(**update_in.member.dict())
#     # .update(gender = update_in.gender)
#     return get_object_or_404(User, id=request.auth['pk'])
#
#
# @clinic_controller.post('ClinicSignin', response={
#     200: ClinicOut,
#     404: MessageOut,
#     400: MessageOut,
# })
# def clinicsignin(request, signin_in: SigninIn):
#     # sign in by phone number
#     user = authenticate(phone_number=signin_in.phone_number, password=signin_in.password)
#     if not user:
#         if not signin_in.email:
#             return 404, {'message': 'User does not exist'}
#
#         # validate email
#         try:
#             validate_email(signin_in.email)
#         except ValidationError:
#             return 400, {'message': 'invalid email'}
#
#         # sign in by email
#         user = get_object_or_404(User, email=signin_in.email)
#         if not check_password(signin_in.password, user.password):
#             return 404, {'message': 'wrong password'}
#     token = create_token(user)
#     if user.account_type == "clinic":
#         return {
#             'profile': user,
#             'token': token,
#         }
#
#
# @clinic_controller.get('all_clinics', response={
#     200: List[ClinicInfo]
# })
# def all_clinic(request):
#     return Clinic.objects.all()
#
#
# @clinic_controller.get('one_clinics', response={
#     200: ClinicInfo
# })
# def one_clinic(request, id: UUID4):
#     return get_object_or_404(Clinic, id= id)
# # @account_controller.post('change-password', auth=AuthBearer(), response={
# #     200: MessageOut,
# #     400: MessageOut
# # })
# # def change_password(request, password_update_in: ChangePasswordSchema):
# #     # user = authenticate(get_object_or_404(User, id=request.auth['pk']).email, password_update_in.old_password)
# #     if password_update_in.new_password1 != password_update_in.new_password2:
# #         return 400, {'detail': 'passwords do not match'}
# #     user = get_object_or_404(User, id=request.auth['pk'])
# #     is_it_him = user.check_password(password_update_in.old_password)
#
# #     if not is_it_him:
# #         return 400, {'detail': 'Dude, make sure you are him!'}
#
# #     user.set_password(password_update_in.new_password1)
# #     user.save()
# #     return {'detail': 'password updated successfully'}

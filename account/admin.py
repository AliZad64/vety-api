from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User 
from account.models import EmailAccount
# Register your models here.


admin.register(EmailAccount,UserAdmin)
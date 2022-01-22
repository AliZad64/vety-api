from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User 
from account.models import EmailAccount, City
# Register your models here.


admin.site.register(EmailAccount)
admin.site.register(City)
from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User 
from account.models import EmailAccount, City, Address, Zone
# Register your models here.

class AbstractedAccount(UserAdmin):
    ordering = ('phone_number',)

admin.site.register(EmailAccount)
admin.site.register(City)
admin.site.register(Zone)
admin.site.register(Address)
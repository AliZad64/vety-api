from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from account.forms import UserAdminChangeForm, UserAdminCreationForm

from account.models import EmailAccount, City, Address, Zone
# Register your models here.

class AbstractedAccount(UserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm


    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('phone_number', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser',)
    list_filter = ('is_superuser', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Personal info', {'fields': (
        'first_name', 'last_name', 'email', 'address', 'account_type')}),
        ('Permissions',
         {'fields': ('is_active', 'is_superuser', 'is_staff', 'is_verified', 'groups')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2')}
         ),
    )
    search_fields = ('first_name', 'last_name', 'phone_number')
    ordering = ('phone_number',)
    filter_horizontal = ()

admin.site.register(EmailAccount, AbstractedAccount)
admin.site.register(City)
admin.site.register(Zone)
admin.site.register(Address)
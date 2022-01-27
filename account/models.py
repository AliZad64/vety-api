from django.db import models
import re
# Create your models here.
from django.contrib.auth.models import UserManager, AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from config.utils.models import Entity
from django.core.validators import RegexValidator, ValidationError

def number_valid(val):
    if re.match(r'^([\s\d]+)$',val):
        raise  ValidationError('only digit numbers')

class EmailAccountManager(UserManager):
    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})

    def create_user(self, first_name, last_name,phone_number, email = None, password=None):
        if not phone_number:
            raise ValueError('user must have phone_number')

        user = self.model(
            phone_number=phone_number,
        )
        user.set_password(password)
        user.first_name = first_name
        user.last_name = last_name
        if email:
            user.email = self.normalize_email(email)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password):
        user = self.model(
            phone_number=phone_number,
        )
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class EmailAccount(AbstractUser, Entity):
    member = "member"
    clinic = "clinic"
    username = models.NOT_PROVIDED
    email = models.EmailField(_('email address'), unique=True, null= True)
    phone_number = models.CharField(max_length=15, unique=True, validators= [RegexValidator(r'^([\s\d]+)$', 'Only digits characters')])
    address = models.ForeignKey('Address', related_name='Addresss', on_delete=models.SET_NULL, null = True , blank = True)
    account_type = models.CharField('type', max_length=255, choices=[
        (member, member),
        (clinic, clinic),
    ], default= member)
    user_image = models.ImageField(null= True , blank= True, upload_to="images/" )
    deleted_at = models.BooleanField(default=False)


    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    objects = EmailAccountManager()

    def __str__(self):
        return self.first_name + self.last_name

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return True

class City(Entity):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Zone(Entity):
    name = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, blank=True , null= True)
    def __str__(self):
        return self.name

class Address(Entity):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)

    def __str__(self):
        return self.city.name + " - " + self.zone.name
from django.db import models

# Create your models here.
from django.contrib.auth.models import UserManager, AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from config.utils.models import Entity
from django.core.validators import RegexValidator



class EmailAccountManager(UserManager):
    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})

    def create_user(self, first_name, last_name, email, password=None):
        if not email:
            raise ValueError('user must have email')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.first_name = first_name
        user.last_name = last_name
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.model(
            email=self.normalize_email(email),
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
    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(_('phone number'),max_length=15, unique=True, null= True , blank = True, validators= [RegexValidator(r'^([\s\d]+)$', 'Only digits characters')])
    city = models.ForeignKey('City', related_name='fromCity', on_delete=models.SET_NULL, null = True , blank = True)
    area = models.CharField('area',max_length=255, null = True , blank=True)
    account_type = models.CharField('type', max_length=255, choices=[
        (member, member),
        (clinic, clinic),
    ], default= member)
    user_image = models.ImageField(null= True , blank= True, upload_to="images/" )
    deleted_at = models.BooleanField(default=False)


    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = EmailAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return True

class City(Entity):
    name = models.CharField(max_length=255)
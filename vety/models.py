import uuid
from django.contrib.auth import get_user_model
from django.db import models

from config.utils.models import Entity


User = get_user_model()

# Create your models here.
class Member(Entity):
    male = "male"
    female = "female"
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField('gender', max_length=255, null = True, blank=True, choices=[
        (male, male),
        (female, female),
    ])
    birth = models.DateField('birth', null=True , blank=True)

class Clinic(Entity):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    facebook = models.URLField('facebook', max_length=500, null=True, blank=True)
    instagram = models.URLField('instagram', max_length=500, null=True, blank=True)
    work_range = models.CharField('work_range',max_length=255, null= True , blank=True)
    



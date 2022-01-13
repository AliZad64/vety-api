import uuid
from django.contrib.auth import get_user_model
from django.db import models

from config.utils.models import Entity


User = get_user_model()

# Create your models here.

# Member and Clinic type of models linked with the django user table
class Member(models.Model):
    male = "male"
    female = "female"
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="memberss")
    gender = models.CharField('gender', max_length=255, null = True, blank=True, choices=[
        (male, male),
        (female, female),
    ])
    birth = models.DateField('birth', null=True , blank=True)

class Clinic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name= "clinicss")
    facebook = models.URLField('facebook', max_length=500, null=True, blank=True)
    instagram = models.URLField('instagram', max_length=500, null=True, blank=True)
    work_range = models.CharField('work_range',max_length=255, null= True , blank=True)
    

#---------blog model---------

class Blog(Entity):
    title = models.CharField('title', max_length=255)
    description = models.TextField('description')
    image = models.CharField('image', max_length=255,blank=True, null=True)
    owner = models.ForeignKey(Clinic, related_name="fromClinic", on_delete=models.CASCADE)
    type = models.ForeignKey('PetType', related_name= "fromPet", null = True , blank = True, on_delete= models.SET_NULL)

#-------pet related models--------
class PetType(Entity):
    name = models.CharField('title', max_length=255)



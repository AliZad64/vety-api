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
    def __str__(self):
        return self.id.phone_number

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

    def __str__(self):
        return self.title
#-------pet related models--------
class PetType(Entity):
    name = models.CharField('title', max_length=255)

    def __str__(self):
        return self.name


class Pet(Entity):
    name = models.CharField('name', max_length=255)
    owner = models.ForeignKey(Member, on_delete=models.CASCADE, related_name= "pet_owner")
    image = models.ImageField('image', blank=True , null=True)
    type_id = models.ForeignKey(PetType, on_delete=models.CASCADE, related_name="pet_type")
    family = models.CharField('family', max_length=255, blank=True , null= True)
    weight = models.IntegerField('weight', blank=True , null=True)
    birth = models.DateField('birth', blank=True, null=True)
    age = models.IntegerField('age', blank=True , null=True)
    clinic_id = models.ManyToManyField(Clinic , related_name='pet_clinic')
    def __str__(self):
        return self.name


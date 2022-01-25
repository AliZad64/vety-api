import uuid
from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.validators import RegexValidator

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
    clinic_name = models.CharField('name',max_length=255,unique=True)
    facebook = models.URLField('facebook', max_length=500, null=True, blank=True)
    instagram = models.URLField('instagram', max_length=500, null=True, blank=True)
    start_date = models.TimeField()
    end_date = models.TimeField()

    def __str__(self):
        return self.clinic_name

#---------blog model---------

class Blog(Entity):
    title = models.CharField('title', max_length=255)
    description = models.TextField('description')
    image = models.ImageField('image', upload_to = "blogs/", null = True , blank = True)
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
    image = models.ImageField('image', blank=True , null=True, upload_to="pets/")
    type = models.ForeignKey(PetType, on_delete=models.CASCADE, related_name="pet_type")
    family = models.CharField('family', max_length=255, blank=True , null= True)
    weight = models.IntegerField('weight', blank=True , null=True)
    adopt_date = models.DateField('birth', blank=True, null=True)
    age = models.IntegerField('age', blank=True , null=True)
    clinic = models.ManyToManyField(Clinic , related_name='pet_clinic')

    def __str__(self):
        return self.name


class RateBlog(Entity):
    blog = models.ForeignKey('blog',on_delete=models.CASCADE)
    member = models.ForeignKey('member', on_delete=models.CASCADE)
    is_like = models.BooleanField()
    is_dislike = models.BooleanField()

class RateClinic(Entity):
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5
    blog = models.ForeignKey(Blog, on_delete= models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    point = models.IntegerField('point', choices=[
        (one,one),
        (two,two),
        (three,three),
        (four,four),
        (five,five),
    ], validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ])

class Vaccine(Entity):
    name = models.CharField('name', max_length=255)
    company = models.CharField('company', max_length=255)
    next = models.DateField('next', null=True, blank=True)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Report(Entity):
    title = models.CharField('title', max_length=255)
    allergy = models.CharField('allergy', max_length=255)
    description = models.CharField('description', max_length=255)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Doctor(Entity):
    name = models.CharField('name', max_length=255)
    phone_number = models.CharField('phone_number', max_length=255, validators= [RegexValidator(r'^([\s\d]+)$', 'Only digits characters')])
    clinic = models.ForeignKey(Clinic,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Appointment(Entity):
    clinic = models.ForeignKey(Clinic, on_delete=models.SET_NULL, blank=True , null=True)
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, blank=True , null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()



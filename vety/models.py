import uuid
from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.validators import RegexValidator
from django.db.models import Count
from config.utils.models import Entity, CustomDateTimeField
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE_CASCADE,HARD_DELETE_NOCASCADE, SOFT_DELETE
from ckeditor.fields import RichTextField

User = get_user_model()

# Create your models here.


# Member and Clinic type of models linked with the django user table
class Member(Entity, SafeDeleteModel):
    _safedelete_policy = HARD_DELETE_NOCASCADE
    male = "male"
    female = "female"
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="memberss")
    gender = models.CharField('gender', max_length=255, null = True, blank=True, choices=[
        (male, male),
        (female, female),
    ])
    birth = models.DateField('birth', null=True , blank=True)

    class Meta():
        verbose_name_plural = "الاعضاء"
        verbose_name = "عضو"

    def __str__(self):
        return self.user.phone_number

class Clinic(Entity):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name= "clinicss")
    clinic_name = models.CharField('name',max_length=255,unique=True)
    facebook = models.URLField('facebook', max_length=500, null=True, blank=True)
    instagram = models.URLField('instagram', max_length=500, null=True, blank=True)
    start_date = models.TimeField()
    end_date = models.TimeField()

    class Meta():
        verbose_name_plural = "العيادات"
        verbose_name = "العيادة"
    @property
    def rating_average(self):
        return self.clinicss_clinic_rating.aggregate(models.Avg('point')).get('point__avg')

    def __str__(self):
        return self.clinic_name

#---------blog model---------

class Blog(Entity):
    title = models.CharField('title', max_length=255)
    description = models.TextField('description')
    image = models.ImageField('image', upload_to = "blogs/")
    owner = models.ForeignKey(User, related_name="fromClinic", on_delete=models.CASCADE)
    type = models.ForeignKey('PetType', related_name= "fromPet", null = True , blank = True, on_delete= models.SET_NULL)

    class Meta():
        verbose_name_plural = "المقالات"
        verbose_name = "المقالة"

    @property
    def like_count(self):
        return self.blogss_rating_like.count()

    @property
    def dislike_count(self):
        return self.blogss_rating_dislike.count()

    def __str__(self):
        return self.title

#-------pet related models--------
class PetType(Entity):
    name = models.CharField('title', max_length=255)

    class Meta():
        verbose_name_plural = "انواع الحيوانات"
        verbose_name = "نوع الحيوان"

    def __str__(self):
        return self.name


class Pet(Entity, SafeDeleteModel):
    _safedelete_policy = HARD_DELETE_NOCASCADE
    male = "male"
    female = "female"
    name = models.CharField('name', max_length=255)
    owner = models.ForeignKey(Member, on_delete=models.CASCADE, related_name= "pet_owner")
    gender = models.CharField('gender', max_length=255, null = True, blank=True, choices=[
        (male, male),
        (female, female),
    ])
    image = models.ImageField('image', blank=True , null=True, upload_to="pets/")
    type = models.ForeignKey(PetType, on_delete=models.CASCADE, related_name="pet_type")
    family = models.CharField('family', max_length=255, blank=True , null= True)
    weight = models.IntegerField('weight', blank=True , null=True)
    adopt_date = models.DateField('birth', blank=True, null=True)
    age = models.IntegerField('age', blank=True , null=True)
    chip_num = models.CharField('chip_number', max_length=255, blank=True , null=True)
    clinic = models.ManyToManyField(Clinic , related_name='pet_clinic')

    class Meta():
        verbose_name_plural = "حيوانات الاليفة"
        verbose_name = "حيوان اليف"

    def __str__(self):
        return self.name + " - " + self.owner.user.phone_number


class LikeBlog(Entity):
    blog = models.ForeignKey('blog',on_delete=models.CASCADE, related_name="blogss_rating_like")
    member = models.ForeignKey('member', on_delete=models.CASCADE, related_name="memberss_rating_like")
    is_like = models.BooleanField(default=False)

    class Meta():
        verbose_name_plural = "اعجاب المقالة"
        verbose_name = "اعجاب المقالة"

class DislikeBlog(Entity):
    blog = models.ForeignKey('blog',on_delete=models.CASCADE, related_name="blogss_rating_dislike")
    member = models.ForeignKey('member', on_delete=models.CASCADE, related_name="memberss_rating_dislike")
    is_dislike = models.BooleanField(default=False)

    class Meta():
        verbose_name_plural = "كره المقالة"
        verbose_name = "كره المقالة"

class RateClinic(Entity):
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5
    clinic = models.ForeignKey(Clinic, on_delete= models.CASCADE, related_name="clinicss_clinic_rating")
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name= "memberss_clinic_rating")
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

    class Meta():
        verbose_name_plural = "تقييمات"
        verbose_name = "تقييم"



class Vaccine(Entity):
    name = models.CharField('name', max_length=255)
    company = models.CharField('company', max_length=255)
    next = models.DateField('next', null=True, blank=True)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="petss_vaccine")
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name = "clinics_vaccine")

    class Meta():
        verbose_name_plural = "اللقاحات"
        verbose_name = "اللقاح"

    def __str__(self):
        return self.name

class Report(Entity):
    title = models.CharField('title', max_length=255)
    allergy = models.CharField('allergy', max_length=255)
    description = models.TextField('description')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="petss_report")
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name="clinicss_report")

    class Meta():
        verbose_name_plural = "التقارير"
        verbose_name = "تقرير"

    def __str__(self):
        return self.title

class Doctor(Entity):
    name = models.CharField('name', max_length=255)
    image = models.ImageField('image', upload_to="doctor/", null = True, blank=True)
    phone_number = models.CharField('phone_number', max_length=255, validators= [RegexValidator(r'^([\s\d]+)$', 'Only digits characters')])
    clinic = models.ForeignKey(Clinic,on_delete=models.CASCADE, related_name="clinicss_doctor")

    class Meta():
        verbose_name_plural = "الاطباء"
        verbose_name = "طبيب"

    def __str__(self):
        return self.name

class Appointment(Entity):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name="clinicss_appointment")
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="memberss_appointment")
    start_date = CustomDateTimeField()
    end_date = CustomDateTimeField()

    class Meta():
        verbose_name_plural = "المواعيد"
        verbose_name = "الموعد"


class Contact(Entity):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField('email address')
    question = models.TextField()

    class Meta():
        verbose_name_plural = "الرسائل"
        verbose_name = "الرسالة"
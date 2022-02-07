from django.contrib import admin
from vety.models import *
from django.utils.safestring import mark_safe

# Register your models here.
class InlineVaccine(admin.StackedInline):
    model = Vaccine
class InlinePet(admin.StackedInline):
    model = Pet
class InlineDoctor(admin.TabularInline):
    model = Doctor
class ClinicAdmin(admin.ModelAdmin):
    inlines = [InlineDoctor, InlineVaccine]
    list_display = ('clinic_name', 'start_date', 'end_date', 'user' , 'rating_average')
    list_filter = ('start_date', 'end_date')
    search_fields = ('clinic_name',)

class BlogAdmin(admin.ModelAdmin):
    list_display = ( 'title','image_show','type', 'owner' , 'like_count', 'dislike_count')
    list_filter = ('type', 'owner')
    search_fields = ('title',)
    readonly_fields = ['image_show']

    def image_show(self, obj):
        return mark_safe('<img src="{url}" width=100 height=100 />'.format(
            url=obj.image.url,
            width=100,
            height=100,
        )
        )
class MemberAdmin(admin.ModelAdmin):
    inlines = [InlinePet]
    list_display = ('user', 'gender')
    list_filter = ('gender',)


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('clinic', 'member', 'start_date', 'end_date')

class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','email')
    readonly_fields = ['question']
admin.site.register(Member, MemberAdmin)
admin.site.register(Clinic, ClinicAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(PetType)
admin.site.register(Pet)
admin.site.register(RateClinic)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Doctor)
admin.site.register(Vaccine)
admin.site.register(Report)
admin.site.register(LikeBlog)
admin.site.register(DislikeBlog)
admin.site.register(Contact, ContactAdmin)








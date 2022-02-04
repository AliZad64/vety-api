from django.contrib import admin
from vety.models import *
from django.utils.safestring import mark_safe

# Register your models here.
class InlineDoctor(admin.TabularInline):
    model = Doctor
class ClinicAdmin(admin.ModelAdmin):
    inlines = [InlineDoctor]
    list_display = ('clinic_name', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date')
    search_fields = ('clinic_name',)

class BlogAdmin(admin.ModelAdmin):
    list_display = ( 'title','image','type', 'owner')
    list_filter = ('type', 'owner')
    search_fields = ('title',)


    def image(self, obj):
        return mark_safe('<img src="{url}" width="50" height="50" />'.format(
            url=obj.image.url,
        )
        )

admin.site.register(Member)
admin.site.register(Clinic, ClinicAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(PetType)
admin.site.register(Pet)
admin.site.register(RateClinic)
admin.site.register(Appointment)
admin.site.register(Doctor)
admin.site.register(Vaccine)
admin.site.register(Report)
admin.site.register(LikeBlog)
admin.site.register(DislikeBlog)







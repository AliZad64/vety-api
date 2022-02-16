from django.contrib import admin
from vety.models import *
from django.utils.safestring import mark_safe

# Register your models here.
class Perma():
    def has_add_permission(self, request):
        return request.user.groups.filter(name='clinic').exists()

    def has_change_permission(self, request, obj=None):
        return request.user.groups.filter(name='clinic').exists()

    def has_delete_permission(self, request, obj=None):
        return request.user.groups.filter(name='clinic').exists()
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
    date_hierarchy = 'created'
    list_display = ( 'title','image_show','type' , 'like_count', 'dislike_count')
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
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user
        return qs if user.is_superuser else Blog.objects.filter(owner_id = user.id)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "owner":
                kwargs["queryset"] = Clinic.objects.filter(user_id = request.user.id)
            return super().formfield_for_foreignkey(db_field, request, **kwargs)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def has_add_permission(self, request):
        return request.user.is_superuser or  request.user.groups.filter(name='clinic').exists()

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.groups.filter(name='clinic').exists()

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or  request.user.groups.filter(name='clinic').exists()
    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.groups.filter(name='clinic').exists()
@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    inlines = [InlinePet]
    list_display = ('user','first_name','last_name', 'gender' )
    list_filter = ('gender',)
    def first_name(self, obj):
        return obj.user.first_name

    def last_name(self, obj):
        return obj.user.last_name

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('clinic', 'member', 'start_date', 'end_date')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user
        return qs if user.is_superuser else Appointment.objects.filter(clinic__user_id = user.id)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "member":
                kwargs["queryset"] = Member.objects.filter(memberss_appointment__clinic__user_id = request.user.id).distinct()
            if db_field.name == "clinic":
                kwargs["queryset"] = Clinic.objects.filter(user_id = request.user.id)
            return super().formfield_for_foreignkey(db_field, request, **kwargs)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def has_add_permission(self, request):
        return request.user.is_superuser or  request.user.groups.filter(name='clinic').exists()

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.groups.filter(name='clinic').exists()

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or  request.user.groups.filter(name='clinic').exists()
    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.groups.filter(name='clinic').exists()
class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','email')
    readonly_fields = ['question']

class VaccineAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'next', 'pet')
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user
        return qs if user.is_superuser else Vaccine.objects.filter(clinic__user_id = user.id)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "pet":
                kwargs["queryset"] = Pet.objects.filter(clinic__user_id = request.user.id).distinct()
            if db_field.name == "clinic":
                kwargs["queryset"] = Clinic.objects.filter(user_id = request.user.id)
            return super().formfield_for_foreignkey(db_field, request, **kwargs)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def has_add_permission(self, request):
        return request.user.is_superuser or  request.user.groups.filter(name='clinic').exists()

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.groups.filter(name='clinic').exists()

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or  request.user.groups.filter(name='clinic').exists()
    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.groups.filter(name='clinic').exists()


class ReportAdmin(admin.ModelAdmin):
    list_display = ("title", "allergy", "description", "pet")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user
        return qs if user.is_superuser else Report.objects.filter(clinic__user_id = user.id)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "pet":
                kwargs["queryset"] = Pet.objects.filter(clinic__user_id = request.user.id).distinct()
            if db_field.name == "clinic":
                kwargs["queryset"] = Clinic.objects.filter(user_id = request.user.id)
            return super().formfield_for_foreignkey(db_field, request, **kwargs)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def has_add_permission(self, request):
        return request.user.is_superuser or  request.user.groups.filter(name='clinic').exists()

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.groups.filter(name='clinic').exists()

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or  request.user.groups.filter(name='clinic').exists()
    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.groups.filter(name='clinic').exists()

class DoctorAdmin(admin.ModelAdmin):
    list_display = ("name", "phone_number",  "clinic")
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user
        return qs if user.is_superuser else Doctor.objects.filter(clinic__user_id = user.id)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "clinic":
                kwargs["queryset"] = Clinic.objects.filter(user_id = request.user.id)
            return super().formfield_for_foreignkey(db_field, request, **kwargs)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def has_add_permission(self, request):
        return request.user.is_superuser or  request.user.groups.filter(name='clinic').exists()

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.groups.filter(name='clinic').exists()

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or  request.user.groups.filter(name='clinic').exists()
    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.groups.filter(name='clinic').exists()

admin.site.register(Clinic, ClinicAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(PetType)
admin.site.register(Pet)
admin.site.register(RateClinic)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Vaccine, VaccineAdmin)
admin.site.register(Report,ReportAdmin)
admin.site.register(LikeBlog)
admin.site.register(DislikeBlog)
admin.site.register(Contact, ContactAdmin)








from django.contrib import admin
from vety.models import *
from django.utils.safestring import mark_safe
from django.db.models import Q

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
    list_filter = ('start_date', 'end_date', )
    search_fields = ('clinic_name',)
    readonly_fields = ['rating_average',]


class BlogAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ( 'title','image_show','type' , 'like_count', 'dislike_count', 'created')
    list_filter = ('type', 'owner')
    search_fields = ('title',)
    readonly_fields = ['image_show', 'like_count', 'dislike_count']

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
                kwargs["queryset"] = User.objects.filter(id = request.user.id)
            return super().formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == "owner":
            clinic = Clinic.objects.all()
            kwargs["queryset"] = User.objects.filter(Q(clinicss__in = clinic) | Q(is_superuser = request.user.is_superuser) )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
# to pick the clinic faster with this way
    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.owner = request.user
        super().save_model(request, obj, form, change)
#so you can't update fields after create
    def get_readonly_fields(self, request, obj=None):
        if obj and not request.user.is_superuser:
            return ["title", "description", "image", "owner", "type"]
        else:
            return []
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
    date_hierarchy = 'created'
    list_display = ('clinic', 'member', 'start_date', 'end_date')
    list_filter = ('member', 'start_date', 'end_date')
    search_fields = ['member',]
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
    date_hierarchy = 'created'

    list_display = ('first_name','last_name','email')
    readonly_fields = ['question']

class VaccineAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'next', 'pet', 'created', 'updated')
    list_filter = ('name', 'company', 'pet')
    search_fields = ('name','pet')
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
    date_hierarchy = 'created'

    list_display = ("title", "allergy", "description", "pet", "created", "updated")
    list_filter = ('title','allergy','pet')
    search_fields = ('title',)
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
class petAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "age", "weight", "type")
    search_fields = ('name',)
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user
        return qs if user.is_superuser else Pet.objects.filter(clinic__user_id = request.user.id)
    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.groups.filter(name='clinic').exists()

class RateClinicAdmin(admin.ModelAdmin):
    list_display = ("clinic", "member", "point", "created" , "updated")

class LikeBlogAdmin(admin.ModelAdmin):
    list_display = ("blog", "member", "is_like", "created" , "updated")
class DislikeBlogAdmin(admin.ModelAdmin):
    list_display = ("blog", "member", "is_dislike", "created" , "updated")
admin.site.register(Clinic, ClinicAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(PetType)
admin.site.register(Pet, petAdmin)
admin.site.register(RateClinic, RateClinicAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Vaccine, VaccineAdmin)
admin.site.register(Report,ReportAdmin)
admin.site.register(LikeBlog, LikeBlogAdmin)
admin.site.register(DislikeBlog, DislikeBlogAdmin)
admin.site.register(Contact, ContactAdmin)








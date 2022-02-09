from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include
from account.controllers.user_controller import account_controller, clinic_controller, address_controller
from vety.controllers.pet_controller import pet_controller
from vety.controllers.blog_controller import blog_controller
from vety.controllers.rateclinic_controller import clinic_rating_controller
from vety.controllers.rateblog_controller import blog_rating_controller
from vety.controllers.appointment_controller import appointment_controller
from vety.controllers.contact_controller import contact_controller
from vety.controllers.vaccine_controller import vaccine_controller, vaccine_clinic_controller
from ninja import NinjaAPI
api = NinjaAPI(
    version='1.0.0',
    title='Vety API v1',
    description='API documentation',
)
api.add_router('auth', account_controller)
api.add_router('address',address_controller)
api.add_router('clinic', clinic_controller)
api.add_router('pet', pet_controller)
api.add_router('blog', blog_controller)
api.add_router('clinic_rating', clinic_rating_controller)
api.add_router('blog_rating', blog_rating_controller)
api.add_router('appointment', appointment_controller)
api.add_router('contact', contact_controller)
api.add_router('vaccine', vaccine_controller)
api.add_router('vaccine_clinic', vaccine_clinic_controller)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls)
]

# if settings.DEBUG:
#     urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include
from account.controllers.user_controller import account_controller

from ninja import NinjaAPI
api = NinjaAPI(
    version='1.0.0',
    title='client API v1',
    description='API documentation',
)
api.add_router('auth', account_controller)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls)
]

# if settings.DEBUG:
#     urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from config import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('maintenance/', include('core.maintenance.urls')),
    path('ecommerce/', include('core.ecommerce.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

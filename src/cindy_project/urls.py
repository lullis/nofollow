from django.conf import settings
from django.urls import path
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    path('', include('cindy.urls')),
    path('', include('web.urls')),
    path('admin/', admin.site.urls)
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

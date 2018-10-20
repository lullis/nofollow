from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin

from core.urls import urlpatterns

urlpatterns.extend([
    url(r'^admin/', admin.site.urls)
])

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from core.urls import urlpatterns

urlpatterns.extend([
    url(r'^api/auth/', include('rest_framework.urls')),
    url(r'^admin/', admin.site.urls),

])

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

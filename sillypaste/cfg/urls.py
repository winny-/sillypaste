from django.contrib import admin
from django.urls import include, path
import django.conf.urls
from sillypaste.web.urls import urlpatterns as web_urlpatterns
from sillypaste.api.urls import urlpatterns as api_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', include('watchman.urls')),
    path('', include(web_urlpatterns)),
    path('', include(api_urlpatterns)),
]


django.conf.urls.handler404 = (
    'sillypaste.web.views.errors.error_404_view'  # noqa: F811
)

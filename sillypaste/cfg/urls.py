from django.contrib import admin
from django.urls import include, path
from django.conf.urls import handler404
from sillypaste.web.urls import urlpatterns as web_urlpatterns
from sillypaste.api.urls import urlpatterns as api_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', include('watchman.urls')),
    path('', include(web_urlpatterns)),
    path('', include(api_urlpatterns)),
]


handler404 = 'sillypaste.web.views.errors.error_404_view'  # noqa: F811

from django.contrib import admin
from django.urls import include, path
from django.conf.urls import handler404
from web.urls import urlpatterns as web_urlpatterns
from api.urls import urlpatterns as api_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', include('watchman.urls')),
    path('', include(web_urlpatterns)),
    path('', include(api_urlpatterns)),
]


handler404 = 'web.views.errors.error_404_view'  # noqa: F811

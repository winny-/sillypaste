from django.contrib import admin
from django.urls import include, path
from web.urls import urlpatterns as web_urlpatterns
from api.urls import urlpatterns as api_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', include('watchman.urls')),
    path('', include(web_urlpatterns)),
    path('', include(api_urlpatterns))
]

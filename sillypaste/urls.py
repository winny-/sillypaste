from django.contrib import admin
from django.urls import include, path
from web.urls import urlpatterns as web_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(web_urlpatterns))
]

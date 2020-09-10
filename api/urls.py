from rest_framework.authtoken.views import obtain_auth_token
from django.urls import include, path
from .routers import router
from .views import logout


urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
    path('api/login/', obtain_auth_token),
    path('api/logout/', logout),
]

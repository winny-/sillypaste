from rest_framework import routers
from .views import UserViewSet, PasteViewSet, ExpiryLogViewSet, LanguageViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'paste', PasteViewSet)
router.register(r'expirylog', ExpiryLogViewSet)
router.register(r'language', LanguageViewSet)

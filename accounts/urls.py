# accounts/urls.py
from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet, CustomUserViewSet

router = DefaultRouter()
router.register(r'companies', CompanyViewSet, basename='company')
router.register(r'users', CustomUserViewSet, basename='user')

urlpatterns = router.urls

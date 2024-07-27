from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IndividualProfileViewSet, CompanyProfileViewSet

router = DefaultRouter()
router.register(r'individuals', IndividualProfileViewSet)
router.register(r'companies', CompanyProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

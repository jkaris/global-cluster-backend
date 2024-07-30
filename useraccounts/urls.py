from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    IndividualProfileViewSet,
    CompanyProfileViewSet,
    CustomTokenObtainPairView,
    SignupView,
    CompanyProfileView,
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r"individuals", IndividualProfileViewSet)
router.register(r"companies", CompanyProfileViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("signup/", SignupView.as_view(), name="signup"),
    # path('login/', LoginView.as_view(), name='login'),
    path("companies/", CompanyProfileView.as_view(), name="company-list"),
]

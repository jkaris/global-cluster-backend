from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductViewSet,
    SupportTicketViewSet,
    UserRankingViewSet,
    VerifyAccountView,
)

router = DefaultRouter()
router.register(r"products", ProductViewSet)
router.register(r"supporttickets", SupportTicketViewSet)
router.register(r"userrankings", UserRankingViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("verify/", VerifyAccountView.as_view(), name="verify-account"),
]

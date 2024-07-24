from django.urls import path
from .views import (
    CompanyCreateView,
    IndividualCreateView,
    LoginView,
    ProductDetailAPIView,
    ProductListCreateAPIView,
    SupportTicketViewSet,
)

urlpatterns = [
    path("register/company/", CompanyCreateView.as_view(), name="register_company"),
    path(
        "register/individual/",
        IndividualCreateView.as_view(),
        name="register_individual",
    ),
    path("login/", LoginView.as_view(), name="login"),
    path("products/", ProductListCreateAPIView.as_view(), name="product-list-create"),
    path("products/<uuid:pk>/", ProductDetailAPIView.as_view(), name="product-detail"),
    path(
        "support-tickets/",
        SupportTicketViewSet.as_view({"get": "list"}),
        name="support-ticket-list",
    ),
]

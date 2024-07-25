from django.urls import path
from .views import (
    CompanyCreateView,
    IndividualCreateView,
    LoginView,
    ProductDetailAPIView,
    ProductListCreateAPIView,
    SupportTicketViewSet,
    UserRankingViewSet,
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
        SupportTicketViewSet.as_view({"get": "list", "post": "create"}),
        name="support-ticket-list",
    ),
    path(
        "support-tickets/<uuid:pk>/",
        SupportTicketViewSet.as_view(
            {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}),
        name="support-ticket-detail",
    ),
    path(
        "user-ranking/",
        UserRankingViewSet.as_view({"get": "list", "post": "create"}),
        name="user-ranking",
    ),
    path(
        "user-ranking/<uuid:pk>/",
        UserRankingViewSet.as_view(
            {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}),
        name="user-ranking-detail",
    ),
]

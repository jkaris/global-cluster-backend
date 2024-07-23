from django.urls import path
from .views import CompanyCreateView, IndividualCreateView, LoginView

urlpatterns = [
    path('register/company/', CompanyCreateView.as_view(), name='register_company'),
    path('register/individual/', IndividualCreateView.as_view(), name='register_individual'),
    path('login/', LoginView.as_view(), name='login'),
]

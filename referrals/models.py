from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("The Email field must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    user_type = models.CharField(
        max_length=20,
        choices=[
            ("individual", "Individual"),
            ("company", "Company"),
            ("admin", "Admin"),
        ],
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Company(CustomUser):
    company_name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    phone_no = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    company_registration_no = models.CharField(max_length=50)

    def __str__(self):
        return self.company_name


class Individual(CustomUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    gender = models.CharField(
        max_length=10, choices=[("male", "Male"), ("female", "Female")]
    )
    phone_no = models.CharField(max_length=20)
    address = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

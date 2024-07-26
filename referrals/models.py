from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from uuid import uuid4
from django.core.validators import (
    MaxValueValidator,
    FileExtensionValidator,
)
from .validators import validate_file_size

User = settings.AUTH_USER_MODEL


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


class Product(models.Model):
    """
    Product model for the referral program.
    """

    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    product_name = models.CharField(max_length=255)
    company = models.ForeignKey(
        Company, on_delete=models.SET_NULL, null=True, blank=True
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    description = models.TextField()
    product_image = models.ImageField(
        blank=True,
        null=True,
        upload_to="product_images/",
        validators=[
            FileExtensionValidator(allowed_extensions=["png", "jpg", "jpeg", "tiff"]),
            validate_file_size,
        ],
    )
    product_link = models.CharField(max_length=255)
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("active", "Active"),
        ("declined", "Declined"),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    shares = models.PositiveIntegerField(
        default=0, validators=[MaxValueValidator(1_000_000_000)]
    )
    traffic = models.PositiveIntegerField(
        default=0, validators=[MaxValueValidator(1_000_000_000)]
    )

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.product_name


class SupportTicket(models.Model):
    """
    Support ticket model for the referral program.
    """

    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    submitted_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="support_tickets"
    )
    SUPPORT_CHOICES = [
        ("support", "Support"),
        ("suggestion", "Suggestion"),
    ]
    support = models.CharField(
        max_length=15, choices=SUPPORT_CHOICES, default="support"
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    STATUS_CHOICES = [
        ("in-progress", "In Progress"),
        ("resolved", "Resolved"),
    ]
    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default="in-progress"
    )
    PRIORITY_CHOICES = [
        ("high", "High"),
        ("medium", "Medium"),
        ("low", "Low"),
    ]
    priority = models.CharField(max_length=15, choices=PRIORITY_CHOICES, default="low")
    attachments = models.FileField(
        blank=True,
        null=True,
        upload_to="support_ticket_attachments/",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["png", "jpg", "jpeg", "tiff", "pdf"]
            ),
            validate_file_size,
        ],
    )

    def __str__(self):
        return self.title


class UserRanking(models.Model):
    """
    User ranking model for the referral program.
    """

    icon = models.ImageField(
        upload_to="ranking_icons/", validators=[validate_file_size]
    )
    user = models.CharField(max_length=255)
    rank_level = models.IntegerField(default=0)
    NAME_CHOICES = [
        ("gold pro", "Gold Pro"),
        ("gold", "Gold"),
        ("silver pro", "Silver Pro"),
        ("silver", "Silver"),
        ("platinum", "Platinum"),
    ]
    name = models.CharField(max_length=15, choices=NAME_CHOICES, default="silver")
    total_recruits = models.IntegerField(default=0)
    bonus = models.IntegerField(default=0)
    STATUS_CHOICES = [
        ("enabled", "Enabled"),
        ("disabled", "Disabled"),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="enabled")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

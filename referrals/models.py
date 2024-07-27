from django.db import models
from uuid import uuid4
from django.core.validators import MaxValueValidator, FileExtensionValidator
from useraccounts.models import CompanyProfile, CustomUser
from .validators import validate_file_size


class Product(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    product_name = models.CharField(max_length=255)
    company = models.ForeignKey(
        CompanyProfile, on_delete=models.CASCADE, related_name="products"
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
    product_value = models.CharField(
        max_length=10,
        choices=[("whatsapp", "Whatsapp"), ("phone", "Phone"), ("website", "Website")],
        default="website",
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
        """
        Meta class for the Product model.
        """

        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        """
        Returns a string representation of the Product object.

        :return: The name of the product.
        :rtype: str
        """
        return self.product_name


class SupportTicket(models.Model):
    """
    A model representing a support ticket.
    """

    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    submitted_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="support_tickets"
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

    def save(self, *args, **kwargs):
        """
        Save the object to the database.

        This method is called when an instance of the class is saved to the database. It generates a UUID for the object if it doesn't already have one and then calls the `save` method of the parent class.

        Parameters:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            None
        """
        if not self.uuid:
            self.uuid = uuid4()
        super().save(*args, **kwargs)

    class Meta:
        """
        Meta class for the SupportTicket model.
        """

        verbose_name = "Support Ticket"
        verbose_name_plural = "Support Tickets"

    def __str__(self):
        """
        Returns a string representation of the object.

        :return: The title of the object.
        :rtype: str
        """
        return self.title


class UserRanking(models.Model):
    """
    User ranking model for the referral program.
    """

    icon = models.ImageField(
        upload_to="ranking_icons/", validators=[validate_file_size],
        blank=True, null=True
    )
    user = models.CharField(max_length=255, blank=True, null=True)
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

    class Meta:
        """
        Meta class for the UserRanking model.
        """

        verbose_name = "User Ranking"
        verbose_name_plural = "User Rankings"

    def __str__(self):
        return self.name

from django.db import models
from uuid import uuid4
from django.core.validators import MaxValueValidator, FileExtensionValidator
from useraccounts.models import CompanyProfile
from .validators import validate_file_size


class Product(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    product_name = models.CharField(max_length=255)
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name="products")
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
    shares = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(1_000_000_000)])
    traffic = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(1_000_000_000)])

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        """
        Returns a string representation of the Product object.

        :return: The name of the product.
        :rtype: str
        """
        return self.product_name

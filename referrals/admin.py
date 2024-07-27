from django.contrib import admin

from .models import Product, SupportTicket


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin class for the Product model.
    """
    list_display = ["product_name", "company", "date_created", "date_updated"]
    list_filter = ["company"]


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    """
    Admin class for the SupportTicket model.
    """
    list_display = ["title", "submitted_by", "date_created", "date_updated"]
    list_filter = ["support", "status", "priority"]

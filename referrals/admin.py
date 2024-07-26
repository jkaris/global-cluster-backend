from django.contrib import admin
from .models import Company, Individual, Product, SupportTicket, UserRanking, UserRegistration, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Number of extra forms to show


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]


admin.site.register(Company)
admin.site.register(Individual)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(SupportTicket)
admin.site.register(UserRanking)
admin.site.register(UserRegistration)

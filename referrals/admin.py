from django.contrib import admin
from .models import Company, Individual, Product, SupportTicket, UserRanking, UserRegistration

admin.site.register(Company)
admin.site.register(Individual)
admin.site.register(Product)
admin.site.register(SupportTicket)
admin.site.register(UserRanking)
admin.site.register(UserRegistration)

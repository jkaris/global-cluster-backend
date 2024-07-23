from django.contrib import admin
from .models import Profile, Product, SupportTicket, Wallet, Payout

# Register your models here.
admin.site.register(Profile)
admin.site.register(Product)
admin.site.register(SupportTicket)
admin.site.register(Wallet)
admin.site.register(Payout)

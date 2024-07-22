from django.contrib import admin
from .models import User, Referral


admin.site.register(User)
admin.site.register(Referral)

### making the admin interface
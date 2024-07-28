from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, IndividualProfile, CompanyProfile
from .forms import UserCreationForm, UserChangeForm


class UserAdmin(BaseUserAdmin):
    """
    Define admin model for custom User model with no email field
    """
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ("email", "name", "user_type", "is_staff", "is_active")
    list_filter = ("user_type", "is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("name", "user_type", "profile_picture", "status")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "name",
                    "user_type",
                    "profile_picture",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(CustomUser, UserAdmin)


@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    """
    Admin class for the CompanyProfile model.
    """
    list_display = (
        "user",
        "company_name",
        "company_registration_number",
        "phone_number",
        "address",
        "country",
    )


@admin.register(IndividualProfile)
class IndividualProfileAdmin(admin.ModelAdmin):
    """
    Admin class for the IndividualProfile model.
    """
    list_display = (
        "user",
        "first_name",
        "last_name",
        "phone_number",
        "address",
        "country",
        "state",
        "city",
    )

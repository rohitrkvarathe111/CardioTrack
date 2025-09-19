from django.contrib import admin
from .models import MedicalOrg, UserProfile


@admin.register(MedicalOrg)
class MedicalOrgAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "identity_no",
        "city",
        "state",
        "country",
        "phone",
        "email",
        "is_active",
        "created_at",
        "updated_at",
    )
    search_fields = ("name", "identity_no", "city", "state", "email")
    list_filter = ("is_active", "country", "state")
    ordering = ("-created_at",)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "user_type",
        "org",
        "first_name",
        "last_name",
        "email",
        "mo_num",
        "address",
        "created_by",
        "updated_by",
        "created_at",
        "updated_at",
    )
    search_fields = ("first_name", "last_name", "email", "mo_num", "user__username")
    list_filter = ("user_type", "org", "created_at")
    ordering = ("-created_at",)

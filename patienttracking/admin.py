from django.contrib import admin
from .models import PatientData

@admin.register(PatientData)
class PatientDataAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "patient",
        "tracking_type",
        "verified",
        "org",
        "created_by",
        "updated_by",
        "created_at",
        "updated_at",
    )
    list_filter = ("tracking_type", "verified", "org")
    search_fields = ("patient__username", "patient__email", "org__name")
    autocomplete_fields = ("patient", "org", "created_by", "updated_by")

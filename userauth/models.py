from django.contrib.auth.models import User
from django.db import models
from django.db import models
from django.utils import timezone

class AuditModel(models.Model):
    created_at = models.DateTimeField(editable=False, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        now = timezone.now()  # Always UTC

        if not self.pk and not self.created_at:
            self.created_at = now
        self.updated_at = now  

        super().save(*args, **kwargs)






class MedicalOrg(AuditModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)  
    identity_no = models.CharField(max_length=50, unique=True)   
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default="India")
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.identity_no})"



class UserProfile(AuditModel):
    class UserTypes(models.TextChoices):
        ORG_ADMIN = "ORG_ADMIN", "Medical Org Admin"
        ORG_USER = "ORG_USER", "Medical Org User"
        PATIENT = "PATIENT", "Patient"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    org = models.ForeignKey(MedicalOrg, on_delete=models.CASCADE, null=True, blank=True)
    user_type = models.CharField(max_length=20, choices=UserTypes.choices)

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True, null=True, blank=True)
    mo_num = models.CharField(max_length=13, null=True, blank=True)

    dob = models.DateField(null=True, blank=True)

    address = models.CharField(max_length=200, null=True, blank=True)



    created_by = models.ForeignKey(
        User, related_name="user_profile_created", on_delete=models.SET_NULL, null=True, blank=True
    )
    updated_by = models.ForeignKey(
        User, related_name="user_profile_updated", on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.user_type})"
from django.db import models
from django.contrib.auth.models import User
from userauth.models import UserProfile, MedicalOrg, AuditModel
from django.core.exceptions import ValidationError


class PatientData(AuditModel):
    class TrackType(models.TextChoices):
        HEARTBEAT = 'HEARTBEAT', 'Heartbeat'
        SUGAR = 'SUGAR', 'Sugar'
        COLESTROL = 'COLESTROL', 'Colestrol'
    
    class UnitOfTrackType(models.TextChoices):
        BPM = 'BPM', 'Beats Per Minute'
        MG_DL_SUGAR = 'MG_DL_SUGAR', 'Milligrams per Deciliter (Sugar)'
        MG_DL_COLESTROL = 'MG_DL_COLESTROL', 'Milligrams per Deciliter (Cholesterol)'

        
    tracking_type = models.CharField(
        max_length=20,
        choices=TrackType.choices,
        null=False
    )

    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="patient")
    verified = models.BooleanField(default=False)
    org = models.ForeignKey(MedicalOrg, on_delete=models.CASCADE, null=True, blank=True)

    value = models.CharField(max_length=20, null=True, blank=True)
    unit = models.CharField(
        max_length=20,
        choices=UnitOfTrackType.choices,
        null=True,
        blank=True
    )

    created_by = models.ForeignKey(
        User, related_name="patient_data_created", on_delete=models.SET_NULL, null=True, blank=True
    )
    updated_by = models.ForeignKey(
        User, related_name="patient_data_updated", on_delete=models.SET_NULL, null=True, blank=True
    )

    def save(self, *args, **kwargs):
        """Auto-fill unit based on tracking_type"""
        if self.tracking_type == self.TrackType.HEARTBEAT:
            self.unit = self.UnitOfTrackType.BPM
        elif self.tracking_type == self.TrackType.SUGAR:
            self.unit = self.UnitOfTrackType.MG_DL_SUGAR
        elif self.tracking_type == self.TrackType.COLESTROL:
            self.unit = self.UnitOfTrackType.MG_DL_COLESTROL

        super().save(*args, **kwargs)


    def clean(self):
        
        if not hasattr(self.patient, "profile"):
            raise ValidationError("Selected user does not have a profile.")
        
        if self.patient.profile.user_type != UserProfile.UserTypes.PATIENT:
            raise ValidationError("PatientData can only be created for users of type PATIENT.")

    def __str__(self):
        return f"{self.patient} - {self.tracking_type}"



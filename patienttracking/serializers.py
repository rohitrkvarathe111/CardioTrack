from rest_framework import serializers
from .models import PatientData

class PatientDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientData
        fields = [
            "id",
            "patient",
            "tracking_type",
            "value",
            "unit",
            "verified",
            "org",
            "created_by",
            "updated_by",
        ]
        read_only_fields = ["unit", "created_by", "updated_by", "org"]

    def create(self, validated_data):
        user_profile = self.context.get("user_profile")
        if not user_profile:
            raise serializers.ValidationError("User profile is required.")

        validated_data["org"] = user_profile.org
        return super().create(validated_data)

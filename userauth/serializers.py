from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, MedicalOrg
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserProfile
from django.db import IntegrityError


class RegisterOrgAdminSerializer(serializers.ModelSerializer):
    org_name = serializers.CharField(write_only=True)
    org_address = serializers.CharField(write_only=True)
    identity_no = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["password", "email", "first_name", "last_name", "org_name", "org_address", "identity_no"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_identity_no(self, value):
        """Prevent duplicate org identity numbers"""
        if MedicalOrg.objects.filter(identity_no=value).exists():
            raise serializers.ValidationError("An organization with this identity_no already exists.")
        return value

    def create(self, validated_data):
        org_name = validated_data.pop("org_name")
        org_address = validated_data.pop("org_address")
        identity_no = validated_data.pop("identity_no")

        org = MedicalOrg.objects.create(
            name=org_name,
            address=org_address,
            identity_no=identity_no
        )

        user = User.objects.create_user(
            username=validated_data["email"],
            password=validated_data["password"],
            email=validated_data.get("email"),
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", "")
        )

        UserProfile.objects.create(
            user=user,
            org=org,
            user_type=UserProfile.UserTypes.ORG_ADMIN,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email
        )

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password.")

        user = authenticate(username=user_obj.username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid email or password.")

        # Generate tokens
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        # Add custom claims (optional)
        access["user_id"] = user.id
        access["email"] = user.email

        # Get profile info
        profile = UserProfile.objects.filter(user=user).first()

        return {
            "refresh": str(refresh),
            "access": str(access),
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "user_type": profile.user_type if profile else None,
                "org_id": profile.org.id if profile and profile.org else None,
                "org_name": profile.org.name if profile and profile.org else None,
            }
        }
    

class RegisterOrgUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["password", "email", "first_name", "last_name"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data, org, user_obj):
        user = User.objects.create_user(
            username=validated_data["email"],
            password=validated_data["password"],
            email=validated_data.get("email"),
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", "")
        )

        UserProfile.objects.create(
            user=user,
            org=org,
            user_type=UserProfile.UserTypes.ORG_USER,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            created_by=user_obj,
            updated_by=user_obj

        )
        return user
    

class RegisterPatientSerializer(serializers.ModelSerializer):
    mo_num = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ["password", "email", "first_name", "last_name", "mo_num", "address"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        mo_num = validated_data.pop("mo_num", "")
        address = validated_data.pop("address", "")
        try:
            user = User.objects.create_user(
                username=validated_data["email"],
                password=validated_data["password"],
                email=validated_data.get("email"),
                first_name=validated_data.get("first_name", ""),
                last_name=validated_data.get("last_name", "")
            )

            UserProfile.objects.create(
                user=user,
                user_type=UserProfile.UserTypes.PATIENT,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                mo_num=mo_num,
                address=address,
                created_by=user,
                updated_by=user
            )

        except IntegrityError as e:
            raise serializers.ValidationError({"detail": str(e)})

        return user
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterOrgAdminSerializer, LoginSerializer, RegisterOrgUserSerializer, RegisterPatientSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile, MedicalOrg
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import ValidationError


class RegisterOrgAdminView(APIView):
    def post(self, request):
        serializer = RegisterOrgAdminSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "Organization Admin registered successfully", "username": user.username},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        auth = JWTAuthentication()
        header = auth.get_header(request)
        if header is None:
            return Response({"detail": "Authorization header missing"}, status=401)

        raw_token = auth.get_raw_token(header)
        validated_token = auth.get_validated_token(raw_token)

        user_id = validated_token.get("user_id")
        try:
            user = User.objects.get(id=user_id)
        except Exception as e:
            return Response({"detail": "User not found", "error": str(e)}, status=404)

        try:
            profile = UserProfile.objects.get(user=user)
        except Exception as e:
            return Response({"detail": "User not found", "error": str(e)}, status=404)

        return Response({
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "user_type": profile.user_type if profile else None,
            "org_id": profile.org.id if profile and profile.org else None,
            "org_name": profile.org.name if profile and profile.org else None,
        })



class RegisterOrgUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user  
        try:
            user_profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            return Response({"detail": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)

        if user_profile.user_type != UserProfile.UserTypes.ORG_ADMIN:
            return Response(
                {"detail": "You are not authorized. Only ORG_ADMIN can add users."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = RegisterOrgUserSerializer(data=request.data)
        if serializer.is_valid():
            new_user = serializer.create(serializer.validated_data, org=user_profile.org, user_obj=user_profile.user)
            return Response(
                {"detail": "User created successfully", "user_id": new_user.id},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        user = request.user  
        try:
            user_profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            return Response({"detail": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)

        if user_profile.user_type != UserProfile.UserTypes.ORG_ADMIN:
            return Response(
                {"detail": "You are not authorized. Only ORG_ADMIN can add users."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        queryset = UserProfile.objects.filter(org=user_profile.org).order_by("-id")

        paginator = PageNumberPagination()
        paginator.page_size = 10  
        page = paginator.paginate_queryset(queryset, request)

        results = [
            {
                "id": u.user.id,
                "email": u.user.email,
                "first_name": u.user.first_name,
                "last_name": u.user.last_name,
                "user_type": u.user_type,
                "org_id" : u.org.id,
                "org_name" : u.org.name,
            }
            for u in page
        ]

        return paginator.get_paginated_response(results)
        


class RegisterPatientView(APIView):

    def post(self, request):
        try:
            serializer = RegisterPatientSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            return Response(
                {"message": "Patient registered successfully", "username": user.username},
                status=status.HTTP_201_CREATED
            )
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
    






        
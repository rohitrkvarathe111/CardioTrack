from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PatientDataSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile, MedicalOrg
from .models import PatientData
from rest_framework.pagination import PageNumberPagination





class PatientDataAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user  
        try:
            user_profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            return Response({"detail": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)

        if user_profile.user_type not in [UserProfile.UserTypes.ORG_ADMIN, UserProfile.UserTypes.ORG_USER]:
            return Response(
                {"detail": "You are not authorized. Only ORG_ADMIN or ORG_USER can access this."},
                status=status.HTTP_403_FORBIDDEN
            )

        email = request.query_params.get("email")
        if not email:
            return Response({"detail": "Email parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            get_user_object = UserProfile.objects.get(email__iexact=email, user_type=UserProfile.UserTypes.PATIENT)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Patient with this email not found."}, status=status.HTTP_404_NOT_FOUND)

        result = {
            "id": get_user_object.user.id,
            "email": get_user_object.email,
            "first_name": get_user_object.first_name,
            "last_name": get_user_object.last_name,
            "user_type": get_user_object.user_type,
            "dob": get_user_object.dob,
        }

        return Response(result, status=status.HTTP_200_OK)
    
    def post(self, request):
        user = request.user  
        try:
            user_profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            return Response({"detail": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)

        if user_profile.user_type not in [UserProfile.UserTypes.ORG_ADMIN, UserProfile.UserTypes.ORG_USER]:
            return Response(
                {"detail": "You are not authorized. Only ORG_ADMIN or ORG_USER can access this."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = PatientDataSerializer(data=request.data, context={"user_profile": user_profile})
        if serializer.is_valid():
            patient_data = serializer.save(created_by=user, updated_by=user)
            return Response(PatientDataSerializer(patient_data).data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class ViewPatientDataAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user  
        try:
            user_profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            return Response({"detail": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)

        if user_profile.user_type == UserProfile.UserTypes.PATIENT:
            
            verify_status = request.query_params.get("verify_status")
            tracking_type = request.query_params.get("tracking_type")
            filters = {"patient": user}

            if verify_status is not None:
                filters["verified"] = verify_status.lower() in ["true", "1"]

            if tracking_type:
                filters["tracking_type"] = tracking_type

            patient_data_qs = PatientData.objects.filter(**filters).order_by("-id")

            paginator = PageNumberPagination()
            paginator.page_size = 10  
            paginated_qs = paginator.paginate_queryset(patient_data_qs, request)

            serializer = PatientDataSerializer(paginated_qs, many=True)
            return paginator.get_paginated_response(serializer.data)

        elif user_profile.user_type in [UserProfile.UserTypes.ORG_ADMIN, UserProfile.UserTypes.ORG_USER]:
            
            patient_email = request.query_params.get("patient_email")
            tracking_type = request.query_params.get("tracking_type")
            if not patient_email:
                return Response({"detail": "patient_email is required"}, status=status.HTTP_400_BAD_REQUEST)
            

            try:
                patient_user = User.objects.get(email=patient_email)
            except User.DoesNotExist:
                return Response({"detail": "Patient with this email does not exist"}, status=status.HTTP_404_NOT_FOUND)
            
            filters = {"patient": patient_user.id}
            if tracking_type:
                filters["tracking_type"] = tracking_type
            
            patient_data_qs = PatientData.objects.filter(**filters, verified=True).order_by("-id")

            paginator = PageNumberPagination()
            paginator.page_size = 10  
            paginated_qs = paginator.paginate_queryset(patient_data_qs, request)

            serializer = PatientDataSerializer(paginated_qs, many=True)
            return paginator.get_paginated_response(serializer.data)
        
        else:
            return Response(
                {"detail": "User Type not exist"}, 
                status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request):
        user = request.user  
        try:
            user_profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            return Response({"detail": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)

        if user_profile.user_type != UserProfile.UserTypes.PATIENT:
            return Response(
                {"detail": "You are not authorized. Only PATIENT can Verified this."},
                status=status.HTTP_403_FORBIDDEN
            )
        record_id = request.data.get("record_id")
        if not record_id:
            return Response(
                {"detail": "Record ID is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            patient_data_obj = PatientData.objects.get(id=record_id, patient=user_profile.user)
        except PatientData.DoesNotExist:
            return Response(
                {"detail": "Patient record not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        if patient_data_obj.verified:
            return Response(
                {"detail": "This record is already verified."},
                status=status.HTTP_400_BAD_REQUEST
            )

        patient_data_obj.verified = True
        patient_data_obj.save()

        return Response(
            {"detail": "Record has been successfully verified."},
            status=status.HTTP_200_OK
        )


        
        

  


            

        







        











    





        
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from userauth.models import UserProfile, MedicalOrg
from .models import PatientData


class PatientDataTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.patient_data_url = reverse("patient_data")
        self.view_patient_data_url = reverse("view_patient_data")

        # Org & Admin
        self.org = MedicalOrg.objects.create(name="CardioOrg", address="Street 1", identity_no="ID001")
        self.admin = User.objects.create_user(username="admin", email="admin@example.com", password="pass123")
        self.admin_profile = UserProfile.objects.create(user=self.admin, org=self.org, user_type=UserProfile.UserTypes.ORG_ADMIN)

        # Org User
        self.org_user = User.objects.create_user(username="orguser", email="orguser@example.com", password="pass123")
        self.org_user_profile = UserProfile.objects.create(user=self.org_user, org=self.org, user_type=UserProfile.UserTypes.ORG_USER)

        # Patient
        self.patient = User.objects.create_user(username="patient", email="patient@example.com", password="pass123")
        self.patient_profile = UserProfile.objects.create(user=self.patient, org=self.org, user_type=UserProfile.UserTypes.PATIENT)

    def get_auth_header(self, user):
        refresh = RefreshToken.for_user(user)
        return {"HTTP_AUTHORIZATION": f"Bearer {str(refresh.access_token)}"}

    # -------------------- PatientDataAPIView --------------------
    def test_get_patient_data_success(self):
        headers = self.get_auth_header(self.admin)
        response = self.client.get(self.patient_data_url, {"email": self.patient.email}, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.patient.email)

    def test_get_patient_data_missing_email(self):
        headers = self.get_auth_header(self.admin)
        response = self.client.get(self.patient_data_url, **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_patient_data_not_found(self):
        headers = self.get_auth_header(self.admin)
        response = self.client.get(self.patient_data_url, {"email": "notfound@example.com"}, **headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_patient_data_forbidden_role(self):
        headers = self.get_auth_header(self.patient)
        response = self.client.get(self.patient_data_url, {"email": self.patient.email}, **headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_patient_data_success(self):
        headers = self.get_auth_header(self.org_user)
        payload = {
            "patient": self.patient.id,
            "tracking_type": "BP",
            "value": "120/80"
        }
        response = self.client.post(self.patient_data_url, payload, format="json", **headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["patient"], self.patient.id)

    def test_post_patient_data_invalid(self):
        headers = self.get_auth_header(self.org_user)
        payload = {"tracking_type": "BP"}  # missing patient & value
        response = self.client.post(self.patient_data_url, payload, format="json", **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # -------------------- ViewPatientDataAPIView --------------------
    def test_patient_view_own_data(self):
        # Create record for patient
        record = PatientData.objects.create(
            patient=self.patient, tracking_type="HR", value="75",
            org=self.org, created_by=self.admin, updated_by=self.admin
        )
        headers = self.get_auth_header(self.patient)
        response = self.client.get(self.view_patient_data_url, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data["results"]), 1)

    def test_org_user_view_patient_data_success(self):
        record = PatientData.objects.create(
            patient=self.patient, tracking_type="BP", value="120/80",
            org=self.org, created_by=self.admin, updated_by=self.admin, verified=True
        )
        headers = self.get_auth_header(self.org_user)
        response = self.client.get(self.view_patient_data_url, {"patient_email": self.patient.email}, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data["results"]), 1)

    def test_org_user_view_patient_data_missing_param(self):
        headers = self.get_auth_header(self.org_user)
        response = self.client.get(self.view_patient_data_url, **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patient_verify_record_success(self):
        record = PatientData.objects.create(
            patient=self.patient, tracking_type="BP", value="110/70",
            org=self.org, created_by=self.admin, updated_by=self.admin, verified=False
        )
        headers = self.get_auth_header(self.patient)
        response = self.client.post(self.view_patient_data_url, {"record_id": record.id}, format="json", **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        record.refresh_from_db()
        self.assertTrue(record.verified)

    def test_patient_verify_record_already_verified(self):
        record = PatientData.objects.create(
            patient=self.patient, tracking_type="BP", value="110/70",
            org=self.org, created_by=self.admin, updated_by=self.admin, verified=True
        )
        headers = self.get_auth_header(self.patient)
        response = self.client.post(self.view_patient_data_url, {"record_id": record.id}, format="json", **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patient_verify_record_not_found(self):
        headers = self.get_auth_header(self.patient)
        response = self.client.post(self.view_patient_data_url, {"record_id": 999}, format="json", **headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_non_patient_cannot_verify(self):
        headers = self.get_auth_header(self.org_user)
        response = self.client.post(self.view_patient_data_url, {"record_id": 1}, format="json", **headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

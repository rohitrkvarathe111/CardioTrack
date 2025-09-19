from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserProfile, MedicalOrg


class AuthTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_org_admin_url = reverse("register_org_admin")
        self.login_url = reverse("login")
        self.me_url = reverse("me")
        self.org_user_url = reverse("org_user")
        self.register_patient_url = reverse("register_patient")

    def get_auth_header(self, user):
        refresh = RefreshToken.for_user(user)
        return {"HTTP_AUTHORIZATION": f"Bearer {str(refresh.access_token)}"}

    def test_register_org_admin_success(self):
        payload = {
            "email": "admin@example.com",
            "password": "testpass123",
            "first_name": "Admin",
            "last_name": "User",
            "org_name": "Test Org",
            "org_address": "123 Street",
            "identity_no": "ORG123",
        }
        response = self.client.post(self.register_org_admin_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("username", response.data)

    def test_register_org_admin_duplicate_identity_no(self):
        org = MedicalOrg.objects.create(name="Test Org", address="123 Street", identity_no="ORG123")
        payload = {
            "email": "admin2@example.com",
            "password": "testpass123",
            "first_name": "Admin2",
            "last_name": "User2",
            "org_name": "Another Org",
            "org_address": "456 Street",
            "identity_no": "ORG123",  # duplicate
        }
        response = self.client.post(self.register_org_admin_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_success(self):
        user = User.objects.create_user(username="testuser", email="test@example.com", password="pass123")
        UserProfile.objects.create(user=user, user_type=UserProfile.UserTypes.ORG_ADMIN)

        payload = {"email": "test@example.com", "password": "pass123"}
        response = self.client.post(self.login_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_login_invalid_credentials(self):
        payload = {"email": "invalid@example.com", "password": "wrongpass"}
        response = self.client.post(self.login_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_detail_authenticated(self):
        user = User.objects.create_user(username="meuser", email="me@example.com", password="pass123")
        profile = UserProfile.objects.create(user=user, user_type=UserProfile.UserTypes.ORG_ADMIN)

        headers = self.get_auth_header(user)
        response = self.client.get(self.me_url, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], user.username)

    def test_user_detail_missing_auth(self):
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_register_org_user_success(self):
        # Create org admin
        admin = User.objects.create_user(username="admin", email="admin@example.com", password="pass123")
        org = MedicalOrg.objects.create(name="Test Org", address="Addr", identity_no="X123")
        UserProfile.objects.create(user=admin, org=org, user_type=UserProfile.UserTypes.ORG_ADMIN)

        headers = self.get_auth_header(admin)
        payload = {
            "email": "newuser@example.com",
            "password": "pass123",
            "first_name": "John",
            "last_name": "Doe"
        }
        response = self.client.post(self.org_user_url, payload, format="json", **headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("user_id", response.data)

    def test_register_org_user_forbidden_if_not_admin(self):
        user = User.objects.create_user(username="normal", email="normal@example.com", password="pass123")
        UserProfile.objects.create(user=user, user_type=UserProfile.UserTypes.PATIENT)

        headers = self.get_auth_header(user)
        payload = {
            "email": "newuser2@example.com",
            "password": "pass123",
            "first_name": "Jane",
            "last_name": "Doe"
        }
        response = self.client.post(self.org_user_url, payload, format="json", **headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_org_users_list(self):
        admin = User.objects.create_user(username="admin2", email="admin2@example.com", password="pass123")
        org = MedicalOrg.objects.create(name="Org2", address="Addr2", identity_no="Y123")
        UserProfile.objects.create(user=admin, org=org, user_type=UserProfile.UserTypes.ORG_ADMIN)

        # Add some users under the same org
        for i in range(3):
            u = User.objects.create_user(username=f"user{i}", email=f"user{i}@example.com", password="pass123")
            UserProfile.objects.create(user=u, org=org, user_type=UserProfile.UserTypes.ORG_USER)

        headers = self.get_auth_header(admin)
        response = self.client.get(self.org_user_url, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data["results"]), 3)

    def test_register_patient_success(self):
        payload = {
            "email": "patient@example.com",
            "password": "pass123",
            "first_name": "Patient",
            "last_name": "One",
            "mo_num": "123456789",
            "address": "Patient Address"
        }
        response = self.client.post(self.register_patient_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("username", response.data)

    def test_register_patient_duplicate_email(self):
        User.objects.create_user(username="pat1", email="patient2@example.com", password="pass123")
        payload = {
            "email": "patient2@example.com",
            "password": "pass123",
            "first_name": "Patient",
            "last_name": "Dup"
        }
        response = self.client.post(self.register_patient_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

from django.urls import path
from .views import RegisterOrgAdminView, LoginView, UserDetailView, RegisterOrgUserView, RegisterPatientView

urlpatterns = [
    path("register_org_admin", RegisterOrgAdminView.as_view(), name="register_org_admin"),
    path("login", LoginView.as_view(), name="login"),
    path("me", UserDetailView.as_view(), name="me"),
    path("org_user", RegisterOrgUserView.as_view(), name="org_user"),
    path("register_patient", RegisterPatientView.as_view(), name="register_patient"),

]



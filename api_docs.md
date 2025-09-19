# API Documentation – CardioTrack

## Register Organization Admin
- Endpoint: POST /api/register_org_admin
- Description: Registers a medical organization admin along with creating the organization.
- Curl Request
```bash
curl --location 'http://127.0.0.1:8000/api/register_org_admin' \
--header 'Content-Type: application/json' \
--data-raw '{
  "email": "texstone@hospital.com",
  "password": "123456789",
  "first_name": "texstone",
  "last_name": "hospital",
  "org_name": "HealthCare Org",
  "org_address": "123 Medical Street",
  "identity_no": "ORG001"
}'

```
- Response
```bash
{
    "message": "Organization Admin registered successfully",
    "username": "texstone@hospital.com"
}
```


## User Login 
- Endpoint: POST /api/login
- Description: Login to get JWT tokens.
- Curl Request
```bash
curl --location 'http://127.0.0.1:8000/api/login' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "texstone@hospital.com",
    "password": "123456789"
}'

```
- Response
```bash
{
    "refresh": "...............",
    "access": "................",
    "user": {
        "id": 10,
        "username": "texstone@hospital.com",
        "email": "texstone@hospital.com",
        "first_name": "texstone",
        "last_name": "hospital",
        "user_type": "ORG_ADMIN",
        "org_id": 4,
        "org_name": "HealthCare Org"
    }
}
```


## Get User Details
- Endpoint: GET /api/me
- Description: Get details of the currently authenticated user.
- Curl Request
```bash
curl --location 'http://127.0.0.1:8000/api/me' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU4Mzc2Nzg1LCJpYXQiOjE3NTgyOTAzODUsImp0aSI6IjE0OTgwNzY3M2Q3MjQ0YTE4YmY2ODBiMzBjZWZjYTVkIiwidXNlcl9pZCI6MTAsImVtYWlsIjoidGV4c3RvbmVAaG9zcGl0YWwuY29tIn0.deOKM_RpeK96iE5GphiwaznydxgnVEHkA8eQ6ky2hFo'

```
- Response
```bash
{
    "user_id": 10,
    "username": "texstone@hospital.com",
    "email": "texstone@hospital.com",
    "first_name": "texstone",
    "last_name": "hospital",
    "user_type": "ORG_ADMIN",
    "org_id": 4,
    "org_name": "HealthCare Org"
}
```

## Create Organization Users
- Endpoint: POST /api/org_user
- Description: Create user for org.  (only ORG_ADMIN).
- Curl Request
```bash
curl --location 'http://127.0.0.1:8000/api/org_user' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU4Mzc2Nzg1LCJpYXQiOjE3NTgyOTAzODUsImp0aSI6IjE0OTgwNzY3M2Q3MjQ0YTE4YmY2ODBiMzBjZWZjYTVkIiwidXNlcl9pZCI6MTAsImVtYWlsIjoidGV4c3RvbmVAaG9zcGl0YWwuY29tIn0.deOKM_RpeK96iE5GphiwaznydxgnVEHkA8eQ6ky2hFo' \
--header 'Content-Type: application/json' \
--data-raw '{
    "password":"123456789",
    "email": "user2@texstone.com", 
    "first_name": "user2@texstone.com", 
    "last_name": "texstone"
}'

```
- Response
```bash
{
    "detail": "User created successfully",
    "user_id": 12
}
```


## List Organization Users
- Endpoint: GET /api/org_user
- Description: Get a paginated list of users in the organization (only ORG_ADMIN).
- Curl Request
```bash
curl --location 'http://127.0.0.1:8000/api/org_user' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU4Mzc2Nzg1LCJpYXQiOjE3NTgyOTAzODUsImp0aSI6IjE0OTgwNzY3M2Q3MjQ0YTE4YmY2ODBiMzBjZWZjYTVkIiwidXNlcl9pZCI6MTAsImVtYWlsIjoidGV4c3RvbmVAaG9zcGl0YWwuY29tIn0.deOKM_RpeK96iE5GphiwaznydxgnVEHkA8eQ6ky2hFo'

```
- Response
```bash
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 11,
            "email": "user1@texstone.com",
            "first_name": "user1",
            "last_name": "texstone",
            "user_type": "ORG_USER",
            "org_id": 4,
            "org_name": "HealthCare Org"
        },
        {
            "id": 10,
            "email": "texstone@hospital.com",
            "first_name": "texstone",
            "last_name": "hospital",
            "user_type": "ORG_ADMIN",
            "org_id": 4,
            "org_name": "HealthCare Org"
        }
    ]
}
```

## Register Patient
- Endpoint: POST /api/register_patient
- Description: Registers a patient with optional medical number and address.
- Curl Request
```bash
curl --location 'http://localhost:8000/api/register_patient' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=w8pdsnCEJiqELCj05RfTmQsXtHYF13Zf5IecC4PFtHAQdCQfyZ3rfu0Cmjrvs8ub' \
--data-raw '{
  "email": "patient3@example.com",
  "password": "123456789",
  "first_name": "patient3",
  "last_name": "Brown",
  "mo_num": "1234567899",
  "address": "456 Patient Lane"
}'

```
- Response
```bash
{
    "message": "Patient registered successfully",
    "username": "patient3@example.com"
}
```





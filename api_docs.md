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

## SEarch Patient Data
- Endpoint: GET /api/patient_data
- Description: ORG_ADMIN or ORG_USER can only serch patient deatils.
- Curl Request
```bash
curl --location 'http://localhost:8000/api/patient_data?email=patient3%40example.com' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU4Mzc4MTk3LCJpYXQiOjE3NTgyOTE3OTcsImp0aSI6ImFkZTM2OTJmNTljMTQyZGY5NTBiOTc5YzI2ZmU0ODU0IiwidXNlcl9pZCI6MTIsImVtYWlsIjoidXNlcjJAdGV4c3RvbmUuY29tIn0.mN9omnmsPMc97L0R8ZWz4tRJW-MmJZIdSS6j_V3XCAM' \
--header 'Cookie: csrftoken=w8pdsnCEJiqELCj05RfTmQsXtHYF13Zf5IecC4PFtHAQdCQfyZ3rfu0Cmjrvs8ub'

```
- Response
```bash
{
    "id": 13,
    "email": "patient3@example.com",
    "first_name": "patient3",
    "last_name": "Brown",
    "user_type": "PATIENT",
    "dob": null
}
```


## Create Patient Data
- Endpoint: POST /api/patient_data
- Description: ORG_ADMIN or ORG_USER can create tracking data for a patient.
- Curl Request
```bash
curl --location 'http://localhost:8000/api/patient_data' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU4Mzc4MTk3LCJpYXQiOjE3NTgyOTE3OTcsImp0aSI6ImFkZTM2OTJmNTljMTQyZGY5NTBiOTc5YzI2ZmU0ODU0IiwidXNlcl9pZCI6MTIsImVtYWlsIjoidXNlcjJAdGV4c3RvbmUuY29tIn0.mN9omnmsPMc97L0R8ZWz4tRJW-MmJZIdSS6j_V3XCAM' \
--header 'Cookie: csrftoken=w8pdsnCEJiqELCj05RfTmQsXtHYF13Zf5IecC4PFtHAQdCQfyZ3rfu0Cmjrvs8ub' \
--data '{
  "patient": 13,
  "tracking_type": "HEARTBEAT",
  "value": "72"
}'

```
- Response
```bash
{
    "id": 6,
    "patient": 13,
    "tracking_type": "HEARTBEAT",
    "value": "72",
    "unit": "BPM",
    "verified": false,
    "org": 4,
    "created_by": 12,
    "updated_by": 12
}
```

## View Patient Data (ORG_ADMIN/ORG_USER)
- Endpoint: POST /api/view_patient_data?patient_email=patient3@example.com
- Description: ORG_ADMIN or ORG_USER can view verified patient data.
- Curl Request
```bash
curl --location 'http://localhost:8000/api/view_patient_data?patient_email=patient1%40example.com&verify_status=true' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU4Mzc4MTk3LCJpYXQiOjE3NTgyOTE3OTcsImp0aSI6ImFkZTM2OTJmNTljMTQyZGY5NTBiOTc5YzI2ZmU0ODU0IiwidXNlcl9pZCI6MTIsImVtYWlsIjoidXNlcjJAdGV4c3RvbmUuY29tIn0.mN9omnmsPMc97L0R8ZWz4tRJW-MmJZIdSS6j_V3XCAM' \
--header 'Cookie: csrftoken=w8pdsnCEJiqELCj05RfTmQsXtHYF13Zf5IecC4PFtHAQdCQfyZ3rfu0Cmjrvs8ub'

```
- Response
```bash
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 3,
            "patient": 8,
            "tracking_type": "SUGAR",
            "value": "10",
            "unit": "MG_DL_SUGAR",
            "verified": true,
            "org": 3,
            "created_by": 4,
            "updated_by": 4
        },
        {
            "id": 2,
            "patient": 8,
            "tracking_type": "HEARTBEAT",
            "value": "60",
            "unit": "BPM",
            "verified": true,
            "org": 3,
            "created_by": 6,
            "updated_by": 6
        }
    ]
}
```

## Verify Patient Data (PATIENT)
- Endpoint: POST /api/register_patient
- Description: PATIENT user can verify their own patient data.
- Curl Request
```bash
curl --location 'http://localhost:8000/api/view_patient_data' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU4Mzc5MTQzLCJpYXQiOjE3NTgyOTI3NDMsImp0aSI6IjE0YjgyNmU1YWUxOTRmNDA4Yjk2YjA2N2IwODU2MTU4IiwidXNlcl9pZCI6MTMsImVtYWlsIjoicGF0aWVudDNAZXhhbXBsZS5jb20ifQ.mWbFaxMT38u-9gAZjyRIooLuxoK20KBwiicBmQ2ef6c' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=w8pdsnCEJiqELCj05RfTmQsXtHYF13Zf5IecC4PFtHAQdCQfyZ3rfu0Cmjrvs8ub' \
--data '{
    "record_id": 6
}'

```
- Response
```bash
{
    "detail": "Record has been successfully verified."
}
```





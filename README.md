# Django Authentication API

## Overview
This project implements a secure authentication system using Django and Django REST Framework (DRF). It includes user registration, login, logout, and a protected endpoint to retrieve user details, all using cookie-based authentication.

## Features
- User registration with email verification via OTP.
- Secure login using HttpOnly cookies.
- Protected user details endpoint.
- Logout functionality.
- CSRF protection enabled.
- Swagger API documentation with automatic CSRF token generation.

## Tech Stack
- **Backend:** Django, Django REST Framework (DRF)
- **Authentication:** Cookie-based authentication with CSRF protection
- **API Documentation:** Swagger (drf-yasg)
- **Database:** SQLite (default, can be configured for PostgreSQL/MySQL)
- **Frontend:** Simple HTML + JavaScript for API testing

---

## Project Setup

### 1. Clone the Repository
```sh
git clone https://github.com/DattatrayBodake25/django-auth-api.git
cd django-auth-api

2. Create a Virtual Environment
sh
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install Dependencies
sh
Copy
Edit
pip install -r requirements.txt
4. Apply Migrations
sh
Copy
Edit
python manage.py migrate
5. Run the Server
sh
Copy
Edit
python manage.py runserver
The API will be available at http://127.0.0.1:8000/

API Endpoints
1. User Registration (OTP Verification)
POST /api/register/
Accepts: email, password
Sends OTP to the provided email.
Example Request:
json
Copy
Edit
{
  "email": "user@example.com",
  "password": "securepassword"
}
Response:
json
Copy
Edit
{
  "message": "OTP sent to email for verification."
}
2. Verify OTP
POST /api/register/verify/
Accepts: email, otp, password
Verifies OTP and creates user.
Example Request:
json
Copy
Edit
{
  "email": "user@example.com",
  "otp": "123456",
  "password": "securepassword"
}
Response:
json
Copy
Edit
{
  "message": "User verified and registered successfully!"
}
3. Login
POST /api/login/
Accepts: email, password
Authenticates user and sets auth_token in cookies.
Example Request:
json
Copy
Edit
{
  "email": "user@example.com",
  "password": "securepassword"
}
Response:
json
Copy
Edit
{
  "message": "Login successful!"
}
4. Get Logged-in User Details
GET /api/me/
Requires authentication via auth_token cookie.
Response:
json
Copy
Edit
{
  "username": "user@example.com",
  "email": "user@example.com"
}
5. Logout
POST /api/logout/
Clears auth_token cookie.
Response:
json
Copy
Edit
{
  "message": "Logout successful!"
}
Security Features
CSRF Protection: CSRF token is required for all requests.
HttpOnly Cookies: auth_token is stored in an HttpOnly, Secure cookie.
OTP Expiry: OTPs expire after 5 minutes.
API Documentation
Swagger UI is available at:

arduino
Copy
Edit
http://127.0.0.1:8000/swagger/
It includes:

Automatic CSRF token generation.
API testing interface.
Frontend (Optional)
A simple frontend (HTML + JavaScript) is included for API testing.

To test:

Open index.html in a browser.
Use the forms to register, verify OTP, login, and fetch user details.
Deployment
For production deployment:

Use PostgreSQL instead of SQLite.
Enable HTTPS and set SECURE_SSL_REDIRECT = True.
Use environment variables for secret keys and sensitive data.

Repository Structure
``` bash
/django-auth-api
│── authentication/         # Django app for authentication
│── templates/              # Contains frontend HTML
│── manage.py               # Django entry point
│── requirements.txt        # Project dependencies
│── README.md               # Documentation
How to Submit
Push your code to GitHub.
Share the GitHub repository link.
Upload a demo video on YouTube (unlisted) and share the link.

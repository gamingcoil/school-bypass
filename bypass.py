import os
import requests
from datetime import datetime

BASE_URL = "https://school-arrival.vercel.app"

USERNAME = os.environ["CTF_USERNAME"]
PASSWORD = os.environ["CTF_PASSWORD"]

# The location used for the CTF
LATITUDE = 32.078100552583216
LONGITUDE = 34.87379928650194
ACCURACY = 124


session = requests.Session()

# --------------------------------------------------
# 1. Get CSRF token
# --------------------------------------------------

response = session.get(f"{BASE_URL}/api/auth/csrf")
response.raise_for_status()

csrf_token = response.json()["csrfToken"]

print("Got CSRF token")


# --------------------------------------------------
# 2. Login using NextAuth Credentials
# --------------------------------------------------

login_data = {
    "identifier": USERNAME,
    "password": PASSWORD,
    "redirect": "false",
    "csrfToken": csrf_token,
    "callbackUrl": f"{BASE_URL}/login",
    "json": "true"
}

response = session.post(
    f"{BASE_URL}/api/auth/callback/credentials",
    data=login_data,
    allow_redirects=False
)

print("Login status:", response.status_code)

if response.status_code not in (200, 302):
    print(response.text)
    raise RuntimeError("Login failed")


# --------------------------------------------------
# 3. Verify that we're authenticated
# --------------------------------------------------

response = session.get(f"{BASE_URL}/api/auth/session")
response.raise_for_status()

session_data = response.json()

print("Session:", session_data)

if not session_data:
    raise RuntimeError("No authenticated session")


# --------------------------------------------------
# 4. Perform check-in
# --------------------------------------------------

checkin_data = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "accuracy": ACCURACY
}

response = session.post(
    f"{BASE_URL}/api/check-in",
    json=checkin_data
)

print("Check-in status:", response.status_code)
print("Response:", response.text)

if response.ok:
    print("Check-in successful!")
else:
    print("Check-in failed")

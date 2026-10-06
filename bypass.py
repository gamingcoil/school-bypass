import os
import requests
from datetime import datetime
from zoneinfo import ZoneInfo

BASE_URL = "https://school-arrival.vercel.app"

USERNAME = os.environ["CTF_USERNAME"]
PASSWORD = os.environ["CTF_PASSWORD"]

LATITUDE = 32.078100552583216
LONGITUDE = 34.87379928650194
ACCURACY = 124


def main():
    session = requests.Session()

    print("Starting check-in...")
    print(
        "Time:",
        datetime.now(ZoneInfo("Asia/Jerusalem")).strftime("%Y-%m-%d %H:%M:%S")
    )

    # ----------------------------------------
    # Get CSRF token
    # ----------------------------------------

    response = session.get(
        f"{BASE_URL}/api/auth/csrf",
        timeout=30
    )

    response.raise_for_status()

    csrf_token = response.json()["csrfToken"]

    print("CSRF token received")


    # ----------------------------------------
    # Login
    # ----------------------------------------

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
        allow_redirects=False,
        timeout=30
    )

    print("Login status:", response.status_code)

    if response.status_code not in (200, 302):
        print(response.text)
        raise RuntimeError("Login failed")


    # ----------------------------------------
    # Verify session
    # ----------------------------------------

    response = session.get(
        f"{BASE_URL}/api/auth/session",
        timeout=30
    )

    response.raise_for_status()

    session_data = response.json()

    if not session_data:
        raise RuntimeError("Authentication session was not created")

    print("Authenticated successfully")


    # ----------------------------------------
    # Check-in
    # ----------------------------------------

    checkin_data = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "accuracy": ACCURACY
    }

    response = session.post(
        f"{BASE_URL}/api/check-in",
        json=checkin_data,
        timeout=30
    )

    print("Check-in status:", response.status_code)
    print("Response:", response.text)

    response.raise_for_status()

    print("Check-in completed successfully")


if __name__ == "__main__":
    main()

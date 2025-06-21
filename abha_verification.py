# abha_verification.py
from utils import get_gateway_token, standard_headers, encrypt_rsa, get_bearer_token
import requests
from config import ABHA_BASE, CLIENT_ID, CLIENT_SECRET
import uuid
from datetime import datetime, timezone


gateway_token = get_gateway_token()
print("✅ Gateway Token fetched.")

token = get_bearer_token(CLIENT_ID, CLIENT_SECRET)
print("✅ Access Token fetched.")

encrypted_abha_number = encrypt_rsa("91-2306-6677-1756", gateway_token)


##Verify using aadhaar no otp
# send otp
def send_otp(token: str, encrypted_abha_number: str):
    url = "https://abhasbx.abdm.gov.in/abha/api/v3/profile/login/request/otp"

    headers = {
        "Authorization": f"Bearer {token}",
        "REQUEST-ID": str(uuid.uuid4()),
        "TIMESTAMP": datetime.utcnow().isoformat() + "Z",
        "Content-Type": "application/json",
    }

    body = {
        "scope": ["abha-login", "aadhaar-verify"],
        "loginHint": "abha-number",
        "loginId": encrypted_abha_number,
        "otpSystem": "aadhaar",
    }

    response = requests.post(url, headers=headers, json=body)

    if response.status_code == 200:
        print("✅ OTP sent successfully!")
        txn_id = response.json().get("txnId")
        print("Transaction ID:", txn_id)
        return txn_id
    else:
        print(f"❌ Error {response.status_code}: {response.text}")
        return None


txn_id = send_otp(token, encrypted_abha_number)
# Verify OTP
otp = input("Enter the OTP: ")
encrypted_otp = encrypt_rsa(otp, gateway_token)


def verify_otp(token: str, txn_id: str, encrypted_otp: str):
    """Send request to verify OTP using txnId and encrypted OTP"""

    url = "https://abhasbx.abdm.gov.in/abha/api/v3/profile/login/verify"

    headers = {
        "Authorization": f"Bearer {token}",
        "REQUEST-ID": str(uuid.uuid4()),
        "TIMESTAMP": datetime.utcnow().isoformat() + "Z",
        "Content-Type": "application/json",
    }

    payload = {
        "scope": ["abha-login", "aadhaar-verify"],
        "authData": {
            "authMethods": ["otp"],
            "otp": {"txnId": txn_id, "otpValue": encrypted_otp},
        },
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        print("✅ OTP Verified Successfully.")
        print("Token:", data.get("token"))
        return data.get("token")
    else:
        print(f"❌ Error {response.status_code}: {response.text}")
        return None


verify_otp(token, txn_id, encrypted_otp)


##Verify using abha number's phone number


def send_otp_abha_number(token: str, encrypted_abha_number: str):
    url = "https://abhasbx.abdm.gov.in/abha/api/v3/profile/login/request/otp"

    headers = {
        "Authorization": f"Bearer {token}",
        "REQUEST-ID": str(uuid.uuid4()),
        "TIMESTAMP": datetime.utcnow().isoformat() + "Z",
        "Content-Type": "application/json",
    }

    body = {
        "scope": ["abha-login", "mobile-verify"],
        "loginHint": "abha-number",
        "loginId": encrypted_abha_number,
        "otpSystem": "abdm",
    }

    response = requests.post(url, headers=headers, json=body)

    if response.status_code == 200:
        print("✅ OTP sent successfully!")
        txn_id = response.json().get("txnId")
        print("Transaction ID:", txn_id)
        return txn_id
    else:
        print(f"❌ Error {response.status_code}: {response.text}")
        return None


txn_id = send_otp_abha_number(token, encrypted_abha_number)


otp = input("Enter the OTP: ")
encrypted_otp = encrypt_rsa(otp, gateway_token)


def verify_otp_abha_number(token: str, txn_id: str, encrypted_otp: str):
    """Send request to verify OTP using txnId and encrypted OTP"""

    url = "https://abhasbx.abdm.gov.in/abha/api/v3/profile/login/verify"

    headers = {
        "Authorization": f"Bearer {token}",
        "REQUEST-ID": str(uuid.uuid4()),
        "TIMESTAMP": datetime.utcnow().isoformat() + "Z",
        "Content-Type": "application/json",
    }

    payload = {
        "scope": ["abha-login", "mobile-verify"],
        "authData": {
            "authMethods": ["otp"],
            "otp": {"txnId": txn_id, "otpValue": encrypted_otp},
        },
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        print("✅ OTP Verified Successfully.")
        print("Token:", data.get("token"))
        return data.get("token")
    else:
        print(f"❌ Error {response.status_code}: {response.text}")
        return None


verify_otp_abha_number(token, txn_id, encrypted_otp)

###Verify using AADHAAR

encrypted_aadhaar_number = encrypt_rsa("521527681066", gateway_token)


def send_otp_aadhaar(token: str, encrypted_aadhaar_number: str):
    url = "https://abhasbx.abdm.gov.in/abha/api/v3/profile/login/request/otp"

    headers = {
        "Authorization": f"Bearer {token}",
        "REQUEST-ID": str(uuid.uuid4()),
        "TIMESTAMP": datetime.utcnow().isoformat() + "Z",
        "Content-Type": "application/json",
    }

    body = {
        "scope": ["abha-login", "aadhaar-verify"],
        "loginHint": "aadhaar",
        "loginId": encrypted_aadhaar_number,
        "otpSystem": "aadhaar",
    }

    response = requests.post(url, headers=headers, json=body)

    if response.status_code == 200:
        print("✅ OTP sent successfully!")
        txn_id = response.json().get("txnId")
        print("Transaction ID:", txn_id)
        return txn_id
    else:
        print(f"❌ Error {response.status_code}: {response.text}")
        return None


txn_id = send_otp_abha_number(token, encrypted_abha_number)


otp = input("Enter the OTP: ")
encrypted_otp = encrypt_rsa(otp, gateway_token)


def verify_otp_aadhaar(token: str, txn_id: str, encrypted_otp: str):
    """Send request to verify OTP using txnId and encrypted OTP"""

    url = "https://abhasbx.abdm.gov.in/abha/api/v3/profile/login/verify"

    headers = {
        "Authorization": f"Bearer {token}",
        "REQUEST-ID": str(uuid.uuid4()),
        "TIMESTAMP": datetime.utcnow().isoformat() + "Z",
        "Content-Type": "application/json",
    }

    payload = {
        "scope": ["abha-login", "aadhaar-verify"],
        "authData": {
            "authMethods": ["otp"],
            "otp": {"txnId": txn_id, "otpValue": encrypted_otp},
        },
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        print("✅ OTP Verified Successfully.")
        print("Token:", data.get("token"))
        return data.get("token")
    else:
        print(f"❌ Error {response.status_code}: {response.text}")
        return None


verify_otp_abha_number(token, txn_id, encrypted_otp)

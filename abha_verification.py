# abha_verification.py
# from utils import get_gateway_token, encrypt_rsa, get_bearer_token
import requests
from config import CLIENT_ID, CLIENT_SECRET
import uuid
from datetime import datetime, timezone



##Verify using aadhaar no otp
# send otp
def send_otp(token: str, encrypted_abha_number: str):
    """
    Send OTP for ABHA number verification using Aadhaar
    """
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


# ##Verify using abha number's phone number


def send_otp_abha_number(token: str, encrypted_abha_number: str):
    """
    Send OTP for ABHA number verification using mobile number
    """
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




def verify_otp_abha_number(token: str, txn_id: str, encrypted_otp: str):
    """Send request to verify OTP using txnId and encrypted OTP for ABHA number"""

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




# ###Verify using AADHAAR




def send_otp_aadhaar(token: str, encrypted_aadhaar_number: str):
    """
    Send OTP for verification using Aadhaar number
    """
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



def verify_otp_aadhaar(token: str, txn_id: str, encrypted_otp: str):
    """Send request to verify OTP using txnId and encrypted OTP for Aadhaar"""

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



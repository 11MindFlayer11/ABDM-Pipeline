# abha_creation.py

from utils import get_gateway_token, encrypt_rsa, get_bearer_token
import requests
from config import ABHA_BASE, CLIENT_ID, CLIENT_SECRET
import uuid
from datetime import datetime, timezone


gateway_token = get_gateway_token()
print("✅ Gateway Token fetched.")

token = get_bearer_token(CLIENT_ID, CLIENT_SECRET)
print("✅ Access Token fetched.")

# Creation of ABHA

##Thru aadhaar OTP

encrypted_aadhaar = encrypt_rsa("521527681066", gateway_token)


# Requeest otp for enrolment
def request_abha_otp(token: str, encrypted_aadhaar: str) -> str:
    """
    Sends OTP to Aadhaar-linked mobile number for ABHA enrolment.

    Args:
        token (str): Bearer token.
        encrypted_aadhaar (str): Aadhaar number encrypted using ABDM public RSA key.

    Returns:
        str: txnId from the response, required for verifying OTP later.
    """

    url = "https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/request/otp"

    headers = {
        "REQUEST-ID": str(uuid.uuid4()),
        "TIMESTAMP": datetime.utcnow().isoformat() + "Z",
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    payload = {
        "scope": ["abha-enrol"],
        "loginHint": "aadhaar",
        "loginId": encrypted_aadhaar,
        "otpSystem": "aadhaar",
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()

    data = response.json()
    txn_id = data.get("txnId")

    print("✅ OTP sent. Transaction ID:", txn_id)
    return txn_id


txn_id = request_abha_otp(token, encrypted_aadhaar)

# enrol by aadhar verification
otp = input("Enter the OTP: ")
otp_value = encrypt_rsa(otp, gateway_token)
mobile = "8839843815"


def enrol_by_aadhaar(token: str, txn_id: str, encrypted_otp: str, mobile: str):
    """
    Verifies OTP and completes ABHA enrollment.

    Args:
        token (str): Bearer token.
        txn_id (str): Transaction ID from OTP request.
        encrypted_otp (str): Encrypted OTP value.
        mobile (str): Aadhaar-linked mobile number (unencrypted).

    Returns:
        dict: Full response including ABHA number, profile, etc.
    """

    url = "https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/enrol/byAadhaar"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "REQUEST-ID": str(uuid.uuid4()),
        "TIMESTAMP": datetime.utcnow().isoformat() + "Z",
    }

    payload = {
        "authData": {
            "authMethods": ["otp"],
            "otp": {
                "timeStamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "txnId": txn_id,
                "otpValue": encrypted_otp,
                "mobile": mobile,
            },
        },
        "consent": {"code": "abha-enrollment", "version": "1.4"},
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()

    print("✅ ABHA enrolment successful.")
    return response.json()


result = enrol_by_aadhaar(token, txn_id, otp_value, mobile)
print(result)
########
# aBHA ADDRESS SUGGETIONS
x_token = result["tokens"]["token"]


def get_abha_address_suggestions(token: str, txn_id: str):
    url = "https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/enrol/suggestion"

    headers = {
        "Authorization": f"Bearer {token}",
        "Transaction_Id": txn_id,
        "REQUEST-ID": str(uuid.uuid4()),
        "TIMESTAMP": datetime.now(timezone.utc)
        .isoformat(timespec="milliseconds")
        .replace("+00:00", "Z"),
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    suggestions = response.json().get("abhaAddressList", [])
    print("✅ ABHA address suggestions:", suggestions)
    return suggestions


suggestions = get_abha_address_suggestions(token, txn_id)
print(suggestions)

# SETTING ABHA ADDRESS


def set_abha_address(token, txn_id, abha_address):
    url = "https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/enrol/abha-address"
    headers = {
        "Authorization": f"Bearer {token}",
        "REQUEST-ID": str(uuid.uuid4()),
        "TIMESTAMP": datetime.now(timezone.utc)
        .isoformat(timespec="milliseconds")
        .replace("+00:00", "Z"),
        "Content-Type": "application/json",
    }
    payload = {"txnId": txn_id, "abhaAddress": abha_address, "preferred": 1}

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()

    data = response.json()
    print("✅ ABHA Address set successfully:", data.get("preferredAbhaAddress"))
    return data


abha_address = "shivanshanand11"
result = set_abha_address(token, txn_id, abha_address)
print(result)


###get profile details
def get_abha_profile(token: str, x_token: str) -> dict:
    url = "https://abhasbx.abdm.gov.in/abha/api/v3/profile/account"

    headers = {
        "Authorization": f"Bearer {token}",
        "X-token": f"Bearer {x_token}",
        "REQUEST-ID": str(uuid.uuid4()),
        "TIMESTAMP": datetime.now(timezone.utc)
        .isoformat(timespec="milliseconds")
        .replace("+00:00", "Z"),
    }

    response = requests.get(url, headers=headers)

    response.status_code == 200
    print("✅ Success! ABHA profile details:")
    return response


result = get_abha_profile(token, x_token)
print(result.text)

###Download ABHA CARD


def download_abha_card(token: str, x_token: str):
    url = "https://abhasbx.abdm.gov.in/abha/api/v3/profile/account/abha-card"

    headers = {
        "Authorization": f"Bearer {token}",
        "X-Token": f"Bearer {x_token}",
        "REQUEST-ID": str(uuid.uuid4()),
        "TIMESTAMP": datetime.now(timezone.utc)
        .isoformat(timespec="milliseconds")
        .replace("+00:00", "Z"),
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    # Save the PDF or image
    with open("abha_card.jpg", "wb") as f:
        f.write(response.content)
    print("✅ ABHA Card downloaded as 'abha_card.pdf'")


download_abha_card(token, x_token)

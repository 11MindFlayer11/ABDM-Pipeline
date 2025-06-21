# abha_creation.py

import requests
import uuid
from datetime import datetime, timezone



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
    # response.raise_for_status()

    data = response.json()
    txn_id = data.get("txnId")

    return txn_id




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
    # response.raise_for_status()

    return response.json()





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
    # response.raise_for_status()

    suggestions = response.json().get("abhaAddressList", [])
    print("✅ ABHA address suggestions:", suggestions)
    return suggestions





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
    # response.raise_for_status()

    data = response.json()
    print("✅ ABHA Address set successfully:", data.get("preferredAbhaAddress"))
    return data




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
    # response.raise_for_status()
    # Save the PDF or image
    with open("abha_card.jpg", "wb") as f:
        f.write(response.content)
    print("✅ ABHA Card downloaded as 'abha_card.jpg'")


# download_abha_card(token, x_token)

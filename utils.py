# utils.py

import uuid
from datetime import datetime
import requests
from config import CLIENT_ID, CLIENT_SECRET, GATEWAY_BASE
import re
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA1
import base64


def get_gateway_token():
    url = "https://healthidsbx.abdm.gov.in/api/v1/auth/cert"
    response = requests.get(url)

    response.status_code == 200
    data = response.text
    # match = re.search(
    #     r"-----BEGIN PUBLIC KEY-----(.*?)-----END PUBLIC KEY-----", data, re.DOTALL
    # )
    # key_base64 = match.group(1).strip().replace("\n", "")
    return data


def get_bearer_token(client_id: str, client_secret: str) -> str:
    url = "https://dev.abdm.gov.in/gateway/v0.5/sessions"

    headers = {
        "Content-Type": "application/json",
        "REQUEST-ID": str(uuid.uuid4()),
        "TIMESTAMP": datetime.datetime.utcnow().isoformat(),
        "X-CM-ID": "sbx",
    }

    payload = {
        "clientId": client_id,
        "clientSecret": client_secret,
        "grantType": "client_credentials",
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()

    access_token = response.json().get("accessToken")
    return access_token


def encrypt_rsa(plain_text: str, public_key_pem: str) -> str:
    """
    Encrypts a string using RSA with OAEP (SHA-1 + MGF1) padding.

    :param plain_text: The string to encrypt.
    :param public_key_pem: The RSA public key in PEM format (string with BEGIN/END).
    :return: Base64-encoded encrypted string.
    """
    public_key = RSA.import_key(public_key_pem)
    cipher = PKCS1_OAEP.new(public_key, hashAlgo=SHA1)

    encrypted_bytes = cipher.encrypt(plain_text.encode("utf-8"))
    return base64.b64encode(encrypted_bytes).decode("utf-8")


###Creation of abha
# Thru aadhaar OTP
import requests
import uuid
import datetime


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

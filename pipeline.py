from utils import get_gateway_token, encrypt_rsa, get_bearer_token
import requests
from config import ABHA_BASE, CLIENT_ID, CLIENT_SECRET
import uuid
from datetime import datetime, timezone
import abha_creation as ac


gateway_token = get_gateway_token()
print("✅ Gateway Token fetched.")

token = get_bearer_token(CLIENT_ID, CLIENT_SECRET)
print("✅ Access Token fetched.")


####ABHA CREATION PIPELINE#####
# Thru Aadhaar

aadhaar_number = input("Enter the Aadhaar number: ")
encrypted_aadhaar = encrypt_rsa(aadhaar_number, gateway_token)

txn_id = ac.request_abha_otp(token, encrypted_aadhaar)

otp = input("Enter the OTP: ")
otp_value = encrypt_rsa(otp, gateway_token)
mobile = input("Enter the mobile number: ")

result = ac.enrol_by_aadhaar(token, txn_id, otp_value, mobile)
print(result)

x_token = result["tokens"]["token"]

suggestions = ac.get_abha_address_suggestions(token, txn_id)
print(suggestions)

abha_address = input("Enter the ABHA address: ")
result = ac.set_abha_address(token, txn_id, abha_address)
print(result)

result = ac.get_abha_profile(token, x_token)
print(result.text)

ac.download_abha_card(token, x_token)

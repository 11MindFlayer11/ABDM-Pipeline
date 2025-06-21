from utils import get_gateway_token, encrypt_rsa, get_bearer_token
import requests
from config import ABHA_BASE, CLIENT_ID, CLIENT_SECRET
import uuid
from datetime import datetime, timezone
import abha_creation as ac
import abha_verification as av


def create_abha_with_aadhaar():
    """Pipeline for creating ABHA using Aadhaar"""
    # Get necessary tokens
    gateway_token = get_gateway_token()
    print("✅ Gateway Token fetched.")

    token = get_bearer_token(CLIENT_ID, CLIENT_SECRET)
    print("✅ Access Token fetched.")

    # Get Aadhaar and encrypt it
    aadhaar_number = input("Enter the Aadhaar number: ")
    encrypted_aadhaar = encrypt_rsa(aadhaar_number, gateway_token)

    # Request and verify OTP
    txn_id = ac.request_abha_otp(token, encrypted_aadhaar)
    otp = input("Enter the OTP: ")
    otp_value = encrypt_rsa(otp, gateway_token)
    mobile = input("Enter the mobile number: ")

    # Enroll using Aadhaar
    try:
        result = ac.enrol_by_aadhaar(token, txn_id, otp_value, mobile)
        if result["isNew"]:
            print("ABHA Number created successfully")
        else:
            print("ABHA already exists")
            x = input("Do you want to download the ABHA card? (y/n): ")
            if x == "y":
                ac.download_abha_card(token, result["tokens"]["token"])
            else:
                return
    except Exception as e:
        print(f"Error: {e}")
        return

    x_token = result["tokens"]["token"]

    # Set ABHA address
    suggestions = ac.get_abha_address_suggestions(token, txn_id)
    print("Available ABHA address suggestions:", suggestions)

    abha_address = input("Enter the ABHA address: ")
    result = ac.set_abha_address(token, txn_id, abha_address)
    print(result)

    # Get profile and download card
    profile = ac.get_abha_profile(token, x_token)
    print(profile.text)
    ac.download_abha_card(token, x_token)


def verify_abha_with_aadhaar():
    """Pipeline for verifying ABHA using Aadhaar number"""
    # Get necessary tokens
    gateway_token = get_gateway_token()
    print("✅ Gateway Token fetched.")

    token = get_bearer_token(CLIENT_ID, CLIENT_SECRET)
    print("✅ Access Token fetched.")

    # Get Aadhaar and encrypt it
    aadhaar_number = input("Enter the Aadhaar number: ")
    encrypted_aadhaar = encrypt_rsa(aadhaar_number, gateway_token)

    # Send and verify OTP
    txn_id = av.send_otp_aadhaar(token, encrypted_aadhaar)
    if txn_id:
        otp = input("Enter the OTP: ")
        encrypted_otp = encrypt_rsa(otp, gateway_token)
        av.verify_otp_aadhaar(token, txn_id, encrypted_otp)


def verify_abha_with_aadhaar_mobile():
    """Pipeline for verifying ABHA using mobile number registered with Aadhaar"""
    # Get necessary tokens
    gateway_token = get_gateway_token()
    print("✅ Gateway Token fetched.")

    token = get_bearer_token(CLIENT_ID, CLIENT_SECRET)
    print("✅ Access Token fetched.")

    # Get ABHA number and encrypt it
    abha_number = input("Enter the ABHA number: ")
    encrypted_abha_number = encrypt_rsa(abha_number, gateway_token)

    # Send and verify OTP
    txn_id = av.send_otp(token, encrypted_abha_number)  # This uses Aadhaar OTP system
    if txn_id:
        otp = input("Enter the OTP received on Aadhaar-linked mobile: ")
        encrypted_otp = encrypt_rsa(otp, gateway_token)
        av.verify_otp(token, txn_id, encrypted_otp)


def verify_abha_with_registered_mobile():
    """Pipeline for verifying ABHA using mobile number registered with ABHA"""
    # Get necessary tokens
    gateway_token = get_gateway_token()
    print("✅ Gateway Token fetched.")

    token = get_bearer_token(CLIENT_ID, CLIENT_SECRET)
    print("✅ Access Token fetched.")

    # Get ABHA number and encrypt it
    abha_number = input("Enter the ABHA number: ")
    encrypted_abha_number = encrypt_rsa(abha_number, gateway_token)

    # Send and verify OTP
    txn_id = av.send_otp_abha_number(
        token, encrypted_abha_number
    )  # This uses ABDM OTP system
    if txn_id:
        otp = input("Enter the OTP received on ABHA-registered mobile: ")
        encrypted_otp = encrypt_rsa(otp, gateway_token)
        av.verify_otp_abha_number(token, txn_id, encrypted_otp)


if __name__ == "__main__":
    print("Choose an operation:")
    print("1. Create new ABHA using Aadhaar")
    print("\nVerify ABHA using:")
    print("2. Aadhaar number")
    print("3. Mobile number registered with Aadhaar")
    print("4. Mobile number registered with ABHA")

    choice = input("\nEnter your choice (1-4): ")

    if choice == "1":
        create_abha_with_aadhaar()
    elif choice == "2":
        verify_abha_with_aadhaar()
    elif choice == "3":
        verify_abha_with_aadhaar_mobile()
    elif choice == "4":
        verify_abha_with_registered_mobile()
    else:
        print("Invalid choice!")

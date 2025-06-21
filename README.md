# ABHA (Ayushman Bharat Health Account) Management System

This project provides a Python-based implementation for creating and verifying ABHA (Ayushman Bharat Health Account) numbers using the ABDM (Ayushman Bharat Digital Mission) Sandbox API.

## Project Structure

```
.
├── README.md
├── config.py              # Configuration settings and API credentials
├── utils.py              # Utility functions for tokens and encryption
├── abha_creation.py      # Functions for ABHA creation process
├── abha_verification.py  # Functions for ABHA verification methods
└── pipeline.py           # Main execution pipeline with user interface
```

## Features

### 1. ABHA Creation
- Create new ABHA number using Aadhaar
- Automatic OTP verification
- ABHA address suggestion and selection
- Profile creation and management
- ABHA card download functionality

### 2. ABHA Verification
Three different verification methods are supported:
1. Using Aadhaar number
2. Using mobile number registered with Aadhaar
3. Using mobile number registered with ABHA

## Setup and Configuration

1. Install required dependencies:
```bash
pip install requests pycryptodome
```

2. Configure your credentials in `config.py`:
```python
GATEWAY_BASE = "https://dev.abdm.gov.in/gateway/v0.5"
ABHA_BASE = "https://abhasbx.abdm.gov.in"
CLIENT_ID = "your_client_id"
CLIENT_SECRET = "your_client_secret"
```

## Usage

Run the main pipeline:
```bash
python pipeline.py
```

The interactive menu will guide you through the following options:
1. Create new ABHA using Aadhaar
2. Verify ABHA using Aadhaar number
3. Verify ABHA using mobile number registered with Aadhaar
4. Verify ABHA using mobile number registered with ABHA

## Key Components

### 1. `utils.py`
- `get_gateway_token()`: Fetches the public key for encryption
- `get_bearer_token()`: Gets authentication token for API calls
- `encrypt_rsa()`: Handles RSA encryption for sensitive data

### 2. `abha_creation.py`
- `request_abha_otp()`: Initiates OTP request for ABHA creation
- `enrol_by_aadhaar()`: Handles ABHA enrollment process
- `get_abha_address_suggestions()`: Gets suggested ABHA addresses
- `set_abha_address()`: Sets the chosen ABHA address
- `get_abha_profile()`: Retrieves ABHA profile details
- `download_abha_card()`: Downloads the ABHA card

### 3. `abha_verification.py`
- `send_otp()`: Sends OTP for ABHA verification
- `verify_otp()`: Verifies OTP for authentication
- `send_otp_abha_number()`: Sends OTP to ABHA-registered mobile
- `verify_otp_abha_number()`: Verifies OTP for ABHA number
- `send_otp_aadhaar()`: Sends OTP to Aadhaar-registered mobile
- `verify_otp_aadhaar()`: Verifies OTP for Aadhaar

### 4. `pipeline.py`
Provides the main execution flow with functions:
- `create_abha_with_aadhaar()`: Complete ABHA creation workflow
- `verify_abha_with_aadhaar()`: Verification using Aadhaar
- `verify_abha_with_aadhaar_mobile()`: Verification using Aadhaar mobile
- `verify_abha_with_registered_mobile()`: Verification using ABHA mobile

## Error Handling

The system includes comprehensive error handling for:
- Invalid Aadhaar numbers
- Incorrect OTP entries
- Network/API failures
- Invalid ABHA numbers
- Failed verifications

## Security Features

1. RSA Encryption for sensitive data:
   - Aadhaar numbers
   - ABHA numbers
   - OTP values

2. Secure token management:
   - Gateway tokens
   - Bearer tokens
   - Session tokens

## API Integration

The project uses the ABDM Sandbox API endpoints:
- `/api/v1/auth/cert`: For gateway token
- `/v0.5/sessions`: For bearer token
- `/api/v3/enrollment/*`: For ABHA creation
- `/api/v3/profile/*`: For verification and profile management

## Output Files

- `abha_card.jpg`: Downloaded ABHA card in JPG format

## Notes

1. This implementation uses the Sandbox environment
2. All sensitive information is properly encrypted
3. The system includes proper error messages and user feedback
4. Each verification method has specific error handling
5. The code follows best practices for API integration

## Error Messages

Common error messages and their meanings:
- "Wrong Aadhaar number": Invalid or non-existent Aadhaar
- "Wrong OTP": Incorrect OTP entered
- "Wrong ABHA number": Invalid or non-existent ABHA
- "ABHA already exists": When trying to create duplicate ABHA

## Future Enhancements

Potential areas for improvement:
1. Add support for additional verification methods
2. Implement rate limiting for OTP attempts
3. Add logging mechanism
4. Add unit tests
5. Implement caching for tokens
6. Add support for bulk operations

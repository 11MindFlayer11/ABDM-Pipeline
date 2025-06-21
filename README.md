# ABDM Milestone 1 Python Pipeline

## Structure
- `abha_creation.py` – handles ABHA number creation (Aadhaar OTP flow)
- `abha_verification.py` – handles ABHA address verification (QR, OTP, etc.)
- `utils.py` – shared logic (token, headers)
- `config.py` – credentials and base URLs

## Usage
1. Set your `CLIENT_ID` and `CLIENT_SECRET` in `config.py`.
2. Run each script separately as needed:

```bash
python abha_creation.py
python abha_verification.py
```
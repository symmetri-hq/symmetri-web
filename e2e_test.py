import json
import urllib.request
import urllib.error
import uuid

# 1. FastAPI Direct Signup
signup_url = "https://symmetri-api.onrender.com/api/auth/signup"
signup_data = json.dumps({
    "first_name": "E2ETest",
    "last_name": "User",
    "email": f"testuser_{uuid.uuid4().hex[:8]}@symmetri.org",
    "password": "Password123!",
    "dob": "1990-01-01",
    "country_of_residence": "US",
    "country_destiny": "MX"
}).encode('utf-8')

signup_req = urllib.request.Request(signup_url, data=signup_data, headers={'Content-Type': 'application/json', 'Origin': 'https://symmetri.org'}, method='POST')
print("--- TESTING FASTAPI SIGNUP ---")
try:
    with urllib.request.urlopen(signup_req) as response:
        print("STATUS:", response.status)
        print("RESPONSE:", response.read().decode())
except urllib.error.HTTPError as e:
    print("STATUS:", e.code)
    print("RESPONSE:", e.read().decode())
except Exception as e:
    print("ERROR:", str(e))

# 2. FX Rate
print("\n--- TESTING FX RATE ---")
rate_url = "https://symmetri-api.onrender.com/api/rates?from_currency=USD&to_currency=MXN"
rate_req = urllib.request.Request(rate_url, headers={'Origin': 'https://symmetri.org'}, method='GET')
try:
    with urllib.request.urlopen(rate_req) as response:
        print("STATUS:", response.status)
        print("RESPONSE:", response.read().decode())
except urllib.error.HTTPError as e:
    print("STATUS:", e.code)
    print("RESPONSE:", e.read().decode())
except Exception as e:
    print("ERROR:", str(e))

# 3. Vercel Signup Proxy
print("\n--- TESTING VERCEL SIGNUP PROXY ---")
vercel_signup_data = json.dumps({
    "firstName": "E2ETest",
    "lastName": "ProxyUser",
    "email": f"testuser_proxy_{uuid.uuid4().hex[:8]}@symmetri.org",
    "password": "Password123!",
    "dob": "1990-01-01",
    "country": "US",
    "phone": "+19995550000"
}).encode('utf-8')

vercel_url = "https://symmetri.org/api/mobile/signup"
vercel_req = urllib.request.Request(vercel_url, data=vercel_signup_data, headers={'Content-Type': 'application/json', 'Origin': 'https://symmetri.org'}, method='POST')
try:
    with urllib.request.urlopen(vercel_req) as response:
        print("STATUS:", response.status)
        print("RESPONSE:", response.read().decode())
except urllib.error.HTTPError as e:
    print("STATUS:", e.code)
    print("RESPONSE:", e.read().decode())
except Exception as e:
    print("ERROR:", str(e))

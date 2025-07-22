import requests

# Gọi API get code trực tiếp
response = requests.get("https://funotp.com/api?action=code&id=687fb7d6adb8b9d6461fcc85&apikey=90gbmipazv1z04m1l54oz2opywcagi3b")
result = response.json()

print(f"Response: {result}")

if result.get("ResponseCode") == 0:
    otp = result.get("Result", {}).get("otp")
    sms = result.get("Result", {}).get("SMS")
    print(f"✅ OTP: {otp}")
    print(f"💬 SMS: {sms}")
else:
    print(f"❌ Code: {result.get('ResponseCode')}")
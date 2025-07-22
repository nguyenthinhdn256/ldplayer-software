import uiautomator2 as u2
import time
import random, subprocess
import logging, time
import requests

logger = logging.getLogger(__name__)

# Kết nối emulator-5556
d = u2.connect('emulator-5556')

def rent_number():
    """Hàm test thuê sim FunOTP - không chỉ định operator"""
    api_key = "90gbmipazv1z04m1l54oz2opywcagi3b"
    base_url = "https://funotp.com/api"
    
    print("🔄 Bắt đầu thuê sim (không chỉ định operator)...")
    
    params = {
        "action": "number",
        "service": "facebook",
        "apikey": api_key
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=10)
        result = response.json()
        
        print(f"📋 Response: {result}")
        
        if result.get("ResponseCode") == 0:
            number = result.get("Result", {}).get("number")
            sim_id = result.get("Result", {}).get("id")
            operator = result.get("Result", {}).get("operator", "Unknown")
            price = result.get("Result", {}).get("price")
            balance = result.get("Result", {}).get("balance")
            
            print(f"✅ THÀNH CÔNG!")
            print(f"📱 Number: {number}")
            print(f"🆔 ID: {sim_id}")
            print(f"📡 Operator: {operator}")
            print(f"💰 Price: {price}")
            print(f"💳 Balance: {balance}")
            
            return {"success": True, "number": number, "id": sim_id}
        else:
            print(f"❌ Thất bại - ResponseCode: {result.get('ResponseCode')}")
            return {"success": False, "error": result.get("ResponseCode")}
            
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return {"success": False, "error": str(e)}

# CHẠY TEST
rent_number()




if d.xpath('//*[@text="Xác nhận số di động của bạn qua WhatsApp"]').exists:
    time.sleep(1)
    if d.xpath('//*[@text="Thử cách khác"]').exists:
        time.sleep(1)
        d.xpath('//*[@text="Thử cách khác"]').click()
        time.sleep(1)
    if d.xpath('//*[@text="Gửi mã qua SMS"]').exists:
        time.sleep(1)
        d.xpath('//*[@text="Gửi mã qua SMS"]').click()
        time.sleep(1)
        d.xpath('//*[@text="Tiếp tục"]').click()



if d.xpath('//*[@text="Xác nhận số di động qua SMS"]').exists:
    time.sleep(1)
    if d.xpath('//*[@text="Thử cách khác"]').exists:
        time.sleep(1)
        d.xpath('//*[@text="Thử cách khác"]').click()
        time.sleep(1)
    if d.xpath('//*[@text="Gửi mã qua SMS"]').exists:
        time.sleep(1)
        d.xpath('//*[@text="Gửi mã qua SMS"]').click()
        time.sleep(1)
        d.xpath('//*[@text="Tiếp tục"]').click()
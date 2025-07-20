import uiautomator2 as u2
import time
import random, subprocess
import logging, time
from typing import Dict, Any

logger = logging.getLogger(__name__)

# Kết nối emulator-5556
d = u2.connect('emulator-5558')

d.app_start("com.windscribe.vpn")

# if d.xpath('//*[@content-desc="Facebook from Meta"]').wait(timeout=10):
#     print("Đã thấy Logo Facebook")
#     time.sleep(1)
#     d.xpath("//android.view.ViewGroup[3]/android.widget.Button[1]").click()

# if d.xpath('//*[@content-desc="Meta logo" or @content-desc="Logo Meta"]').exists:
#     print("Đã thấy Logo Facebook")
#     time.sleep(1)
#     d.xpath('//*[@text="Create new account"] | //android.view.ViewGroup[3]/android.widget.Button[1] | //*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[2]/android.widget.FrameLayout[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.widget.Button[1]').click()

# if d.xpath('//*[@text="Hãy tạo tài khoản để kết nối với bạn bè, người thân và cộng đồng có chung sở thích."]').wait(timeout=10):
#     print("Đã thấy Hãy Tạo Tài Khoản")
#     time.sleep(1)
#     d.xpath("//android.view.ViewGroup[1]/android.widget.Button[1]").click()

# if d(text="Bạn tên gì?").wait(timeout=5):
#     d.xpath('//*[@text="Tiếp"]').click()
# if d.xpath('//*[@resource-id="android:id/button1"]').wait(timeout=5):
#     print("Button SET xuất hiện")
#     time.sleep(1)
#     d.xpath('//*[@resource-id="android:id/button1"]').click()


# if d.xpath('//*[@text="Ngày sinh của bạn là khi nào?"]').wait(timeout=5):
#     print("Ngày sinh của bạn là khi nào?")
#     time.sleep(1)
#     d.xpath('//*[@text="Tiếp"]').click()
#     time.sleep(1)
#     d.xpath('//*[@text="Tiếp"]').click()
#     time.sleep(3)
#     age = random.randint(18, 38)
#     d(className="android.widget.EditText").send_keys(str(age))
#     time.sleep(1)
#     d.xpath('//*[@text="Tiếp"]').click()
#     time.sleep(2)
#     d.xpath('//*[@text="OK"]').click()
    
# if d.xpath('//*[@text="Giới tính của bạn là gì?"]').wait(timeout=5):
#     print("Giới tính của bạn là gì?")
#     gender = random.choice(["Nam", "Nữ"])
#     time.sleep(1)
#     d.xpath(f'//*[@text="{gender}"]').click()
#     time.sleep(1)
#     d.xpath('//*[@text="Tiếp"]').click()
    
# # Lấy random họ
# with open('dulieu/hoten/Ho.txt', 'r', encoding='utf-8') as f:
#     ho_list = [line.strip() for line in f.readlines() if line.strip() and not line.startswith('#')]
#     random_ho = random.choice(ho_list)
# with open('dulieu/hoten/Ten.txt', 'r', encoding='utf-8') as f:
#     ten_list = [line.strip() for line in f.readlines() if line.strip() and not line.startswith('#')]
#     random_ten = random.choice(ten_list)    
# **ĐỌC PROXY DATA - NGẮN GỌN**
def setup_proxy(device, device_index=0, **kwargs) -> Dict[str, Any]:
    """Thiết lập WW Proxy - khởi chạy app và đọc proxy data"""
    try:
        logger.info("Setting up WW Proxy on device...")
        
        # ĐỌC PROXY DATA
        proxy_file = f"Profile/Profile-{device_index + 1}/wwproxy.txt"
        with open(proxy_file, 'r', encoding='utf-8') as f:
            proxies = [line.strip() for line in f.readlines() if line.strip()]
        
        proxy_data = proxies[device_index % len(proxies)] if proxies else ""
        logger.info(f"Using proxy: {proxy_data}")
        d.set_clipboard(proxy_data)
        # Khởi chạy app WW Proxy
        device.app_start('com.hct.myapplication')
        
        import time
        time.sleep(5)

        d.xpath('//*[@resource-id="com.hct.myapplication:id/btnPaste"]').click()
        time.sleep(1)
        if device(text="TẮT").exists:
            device(text="TẮT").click()
        time.sleep(2)
        if device(text="OK").exists:
            device(text="OK").click()


        return { "success": True, "provider": "WW Proxy", "proxy_data": proxy_data, "message": "WW Proxy setup completed" }
        
    except Exception as e:
        logger.error(f"Error setting up WW Proxy: {str(e)}")
        return {"success": False, "error": str(e)}


result = setup_proxy(d, device_index=0)
print("Proxy Result:", result)


import uiautomator2 as u2
import time
import random, subprocess
import logging, time
import sys
import os

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Kết nối emulator-5556
d = u2.connect('emulator-5556')

d.xpath('//*[@resource-id="com.hct.myapplication:id/menu_item_switch"]').click()
# ports = ['5556', '5558', '5560', '5562', '5564', '5566', '5568', '5570', '5572']  # thêm các port bạn muốn
# devices = [u2.connect(f'emulator-{port}') for port in ports]


# for port in ports:
#     result = subprocess.run(["adb", "-s", f"emulator-{port}", "shell", "pm", "clear", "com.hct.myapplication"],
#                             capture_output=True, text=True)
#     print(f"[{port}] Clear result:", result.stdout.strip())

# for d in devices:
#     d.app_start('com.facebook.katana')

# time.sleep(5)


# import uiautomator2 as u2
# import time
# import random, subprocess
# import logging, time
# import sys
# import os

# # Thêm đường dẫn đến thư mục service
# sys.path.append(os.path.join(os.path.dirname(__file__), 'service'))

# from service.veri_facebook import FunOTPHandler

# # Setup logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)

# # Kết nối emulator-5556
# d = u2.connect('emulator-5556')

# # **GỌI FUNCTION execute_verification**
# try:
#     # API key thật của bạn
#     api_key = "90gbmipazv1z04m1l54oz2opywcagi3b"
    
#     print(f"🔄 Khởi tạo FunOTP handler...")
#     funotp_handler = FunOTPHandler(api_key=api_key)
    
#     device_id = 'emulator-5556'
#     device_index = 0
    
#     print(f"🔄 Bắt đầu execute_verification với device {device_id}")
#     result = funotp_handler.execute_verification(d, device_id, device_index)
    
#     print(f"📋 Execute verification result: {result}")
    
#     if result.get("success"):
#         print("🎉 VERIFICATION THÀNH CÔNG!")
#         print(f"📱 Phone: {result.get('phone', 'N/A')}")
#         print(f"🔢 OTP: {result.get('otp', 'N/A')}")
#         print(f"💬 Message: {result.get('message', 'N/A')}")
#     else:
#         print("❌ VERIFICATION THẤT BẠI!")
#         print(f"🚨 Error: {result.get('error')}")
    
# except Exception as e:
#     print(f"💥 Exception occurred: {e}")
#     logger.error(f"Error in execute_verification: {e}")
#     import traceback
#     traceback.print_exc()

# print("🏁 Test completed!")
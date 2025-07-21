import uiautomator2 as u2
import time
import random, subprocess
import logging, time
from typing import Dict, Any

logger = logging.getLogger(__name__)

# Kết nối emulator-5556
# d = u2.connect('emulator-5558')

ports = ['5556', '5558', '5560', '5562', '5564', '5566', '5568', '5570', '5572']  # thêm các port bạn muốn
devices = [u2.connect(f'emulator-{port}') for port in ports]


for port in ports:
    result = subprocess.run(["adb", "-s", f"emulator-{port}", "shell", "pm", "clear", "com.facebook.katana"],
                            capture_output=True, text=True)
    print(f"[{port}] Clear result:", result.stdout.strip())

for d in devices:
    d.app_start('com.facebook.katana')

time.sleep(5)



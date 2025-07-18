import uiautomator2 as u2
import time
import random

# Kết nối emulator-5556
d = u2.connect('emulator-5558')

if d(text="Hãy tạo tài khoản để kết nối với bạn bè, người thân và cộng đồng có chung sở thích.").wait(timeout=7):
    time.sleep(1)  
    d(className="android.widget.Button", index=2).click()

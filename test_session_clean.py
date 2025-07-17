import uiautomator2 as u2
import time

# Kết nối emulator-5556
d = u2.connect('emulator-5556')

d.app_stop('com.android.settings')

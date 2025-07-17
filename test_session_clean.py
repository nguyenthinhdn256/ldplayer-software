# test_session_clean.py
from appium import webdriver

caps = {
    'platformName': 'Android',
    'automationName': 'UiAutomator2',
    'deviceName': 'emulator-5556',
    'udid': 'emulator-5556',
    'autoGrantPermissions': True,
    'newCommandTimeout': 60,
    'noReset': True
    # Bỏ systemPort để Appium tự động chọn port có sẵn
}

try:
    print("Đang thử tạo session...")
    driver = webdriver.Remote('http://127.0.0.1:4724', caps)
    print(f"✅ Tạo session thành công: {driver.session_id}")
    
    print("Đang lấy thông tin thiết bị...")
    print(f"Phiên bản platform: {driver.capabilities.get('platformVersion', 'Không xác định')}")
    print(f"Device: {driver.capabilities.get('deviceName', 'Không xác định')}")
    
    # Test một số thao tác cơ bản
    print("Đang test thao tác cơ bản...")
    print(f"Screen size: {driver.get_window_size()}")
    
    driver.quit()
    print("✅ Đóng session thành công")
except Exception as e:
    print(f"❌ Lỗi: {e}")
    import traceback
    traceback.print_exc()
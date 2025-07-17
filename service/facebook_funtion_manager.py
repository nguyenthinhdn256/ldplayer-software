import subprocess, time
import logging
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy

logger = logging.getLogger(__name__)

class XuLyBuoc1:
    """Class xử lý bước 1 trong quá trình tạo tài khoản Facebook"""
    
    def __init__(self, device_id: str):
        self.device_id = device_id
        self.logger = logging.getLogger(__name__)
    
    def thay_doi_ngon_ngu(self) -> dict:
        """Thay đổi ngôn ngữ thiết bị sang tiếng Việt"""
        return change_device_language_to_vietnamese(self.device_id)
    
    def thay_doi_thong_tin_thiet_bi(self, appium_url: str) -> dict:
        """Thay đổi thông tin thiết bị bằng MaxChanger"""
        return change_device_info(self.device_id, appium_url)

def change_device_language_to_vietnamese(device_id: str) -> dict:
    try:
        logger.info(f"Changing language to Vietnamese for device: {device_id}")
        
        # Bước 1: Cấp quyền cho ứng dụng ADB Change Language
        grant_cmd = ["adb", "-s", device_id, "shell", "pm", "grant", "net.sanapeli.adbchangelanguage", "android.permission.CHANGE_CONFIGURATION"]
        grant_result = subprocess.run(grant_cmd, capture_output=True, text=True, timeout=30)
        logger.info(f"Grant permission result for {device_id}: {grant_result.returncode}")

        time.sleep(2)
        
        # Bước 2: Thay đổi ngôn ngữ sang tiếng Việt
        change_cmd = ["adb", "-s", device_id, "shell", "am", "start", "-n", "net.sanapeli.adbchangelanguage/.AdbChangeLanguage", "-e", "language", "vi"]
        change_result = subprocess.run(change_cmd, capture_output=True, text=True, timeout=30)
        logger.info(f"Change language result for {device_id}: {change_result.returncode}")
        
        return {"success": True, "message": f"Language changed to Vietnamese for device {device_id}", "grant_returncode": grant_result.returncode, "change_returncode": change_result.returncode}
        
    except subprocess.TimeoutExpired:
        logger.error(f"Timeout when changing language for device {device_id}")
        return {"success": False, "message": f"Timeout when changing language for device {device_id}"}
    except Exception as e:
        logger.error(f"Error changing language for device {device_id}: {str(e)}")
        return {"success": False, "message": f"Error changing language for device {device_id}: {str(e)}"}

def change_device_info(device_id: str, appium_url: str) -> dict:
    """Thay đổi thông tin thiết bị bằng app MaxChanger - SỬ DỤNG SESSION ĐÃ CÓ"""
    try:
        logger.info(f"Starting device info change for device: {device_id}")
        
        # Lấy session đã tạo sẵn từ AppiumServerManager
        from gui.groupbox_2 import Groupbox2Manager
        # Cần truy cập đến appium_manager instance để lấy session
        # Session đã được tạo khi khởi động server
        
        # Tạm thời dùng session mới vì cần refactor để access manager
        caps = {'platformName': 'Android', 'automationName': 'UiAutomator2', 'deviceName': device_id, 'udid': device_id, 'autoGrantPermissions': True, 'newCommandTimeout': 60, 'noReset': True}

        driver = webdriver.Remote(appium_url, caps)
        logger.info(f"Using session for MaxChanger on device {device_id}")
        
        # Đợi app khởi động
        time.sleep(3)
        
        # Tìm và click button CHANGE INFO
        button = driver.find_element(MobileBy.XPATH, "//android.widget.Button[@text='CHANGE INFO']")
        button.click()
        logger.info(f"Clicked CHANGE INFO button for device {device_id}")
        
        # Đợi xử lý
        time.sleep(2)
        
        # Đóng session
        driver.quit()
        logger.info(f"Device info change completed for device {device_id}")
        
        return {"success": True, "message": f"Device info changed successfully for device {device_id}"}
        
    except Exception as e:
        logger.error(f"Error changing device info for device {device_id}: {str(e)}")
        return {"success": False, "message": f"Error changing device info for device {device_id}: {str(e)}"}
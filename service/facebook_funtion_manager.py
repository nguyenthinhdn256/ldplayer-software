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
    
    def clear_and_capquyen_app(self, app_packages: list = None) -> dict:
        """Clear dữ liệu và cấp quyền storage cho các app"""
        return clear_and_capquyen_app(self.device_id, app_packages)
    
    def wait_facebook_app(self) -> dict:
        """Funtion đợi app facebook load thanh công"""
        return wait_for_facebook_fully_loaded(self.device_id)
    
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

def clear_and_capquyen_app(device_id: str, app_packages: list = None) -> dict:
    """Clear dữ liệu và cấp quyền storage cho các app"""
    try:
        logger.info(f"Clearing data and granting permissions for device: {device_id}")
        
        # Danh sách app mặc định nếu không được cung cấp
        if app_packages is None:
            app_packages = ["com.facebook.katana", "com.facebook.orca", "com.android.chrome", "com.google.android.gms"]
        
        # Clear data cho tất cả apps
        for package in app_packages:
            try:
                clear_cmd = ["adb", "-s", device_id, "shell", "pm", "clear", package]
                subprocess.run(clear_cmd, capture_output=True, text=True, timeout=15)
                logger.info(f"Cleared data for {package} on {device_id}")
            except Exception as e:
                logger.warning(f"Failed to clear {package} on {device_id}: {e}")
        
        # Cấp quyền READ_EXTERNAL_STORAGE và WRITE_EXTERNAL_STORAGE cho tất cả apps
        permissions = ["android.permission.READ_EXTERNAL_STORAGE", "android.permission.WRITE_EXTERNAL_STORAGE"]
        for package in app_packages:
            for permission in permissions:
                try:
                    grant_cmd = ["adb", "-s", device_id, "shell", "pm", "grant", package, permission]
                    subprocess.run(grant_cmd, capture_output=True, text=True, timeout=10)
                    logger.info(f"Granted {permission} to {package} on {device_id}")
                except Exception as e:
                    logger.warning(f"Failed to grant {permission} to {package} on {device_id}: {e}")
        
        return {"success": True, "message": f"Cleared data and granted permissions for {len(app_packages)} apps on {device_id}", "processed_apps": app_packages}
        
    except Exception as e:
        logger.error(f"Error in clear_and_capquyen_app for {device_id}: {str(e)}")
        return {"success": False, "message": f"Error in clear_and_capquyen_app for {device_id}: {str(e)}"}
    
# Funtion đợi app facebook load thanh công    
def wait_for_facebook_fully_loaded(d, timeout=60):
    """Chờ Facebook khởi động hoàn toàn"""
    
    # Bước 1: Chờ app chạy foreground
    print("Đang chờ Facebook khởi động...")
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            current_app = d.app_current()
            if current_app.get('package') == 'com.facebook.katana':
                print("✅ Facebook đã chạy foreground")
                break
        except:
            pass
        time.sleep(1)
    else:
        print("❌ Facebook không khởi động trong thời gian quy định")
        return False
    
    # Bước 2: Chờ UI elements xuất hiện
    print("Đang chờ UI Facebook load...")
    time.sleep(2)  # Cho app ổn định
    
    ui_selectors = [{'method': 'text', 'value': 'Đăng ký Facebook'}, {'method': 'text', 'value': 'Tạo tài khoản mới'}, {'method': 'text', 'value': 'Đăng nhập'}, {'method': 'resourceId', 'value': 'com.facebook.katana:id/login_button'}, {'method': 'className', 'value': 'android.widget.Button'}]
    for _ in range(20):  # Thử 20 lần, mỗi lần 1s
        for selector in ui_selectors:
            try:
                if selector['method'] == 'text':
                    if d(text=selector['value']).exists:
                        print(f"✅ UI element tìm thấy: {selector['value']}")
                        return True
                elif selector['method'] == 'resourceId':
                    if d(resourceId=selector['value']).exists:
                        print(f"✅ UI element tìm thấy: {selector['value']}")
                        return True
                elif selector['method'] == 'className':
                    if d(className=selector['value']).exists:
                        print(f"✅ UI element tìm thấy: {selector['value']}")
                        return True
            except:
                continue
        time.sleep(1)
    
    print("❌ Facebook UI không load đầy đủ")
    return False


# def wait_for_facebook_fully_loaded(d, timeout=60):
#     """Chờ Facebook khởi động hoàn toàn và in ra kết quả phát hiện được"""
    
#     # Bước 1: Chờ app chạy foreground
#     print("Đang chờ Facebook khởi động...")
#     start_time = time.time()
    
#     while time.time() - start_time < timeout:
#         try:
#             current_app = d.app_current()
#             if current_app.get('package') == 'com.facebook.katana':
#                 print("✅ Facebook đã chạy foreground")
#                 break
#         except:
#             pass
#         time.sleep(1)
#     else:
#         print("❌ Facebook không khởi động trong thời gian quy định")
#         return False
    
#     # Bước 2: Chờ UI elements xuất hiện
#     print("Đang chờ UI Facebook load...")
#     time.sleep(2)  # Cho app ổn định
    
#     ui_selectors = [
#         {'method': 'text', 'value': 'Đăng ký Facebook'},
#         {'method': 'text', 'value': 'Tạo tài khoản mới'},
#         {'method': 'text', 'value': 'Đăng nhập'},
#         {'method': 'resourceId', 'value': 'com.facebook.katana:id/login_button'},
#         {'method': 'className', 'value': 'android.widget.Button'}
#     ]
    
#     found_elements = []  # Danh sách lưu các element đã tìm thấy
    
#     for attempt in range(20):  # Thử 20 lần, mỗi lần 1s
#         for selector in ui_selectors:
#             try:
#                 if selector['method'] == 'text':
#                     if d(text=selector['value']).exists:
#                         element_info = selector['value']
#                         if element_info not in found_elements:
#                             found_elements.append(element_info)
#                             print(f"✅ Text element tìm thấy: '{element_info}'")
                        
#                 elif selector['method'] == 'resourceId':
#                     if d(resourceId=selector['value']).exists:
#                         element_info = selector['value']
#                         if element_info not in found_elements:
#                             found_elements.append(element_info)
#                             print(f"✅ ResourceId element tìm thấy: '{element_info}'")
                        
#                 elif selector['method'] == 'className':
#                     if d(className=selector['value']).exists:
#                         element_info = selector['value']
#                         if element_info not in found_elements:
#                             found_elements.append(element_info)
#                             print(f"✅ ClassName element tìm thấy: '{element_info}'")
                            
#             except Exception as e:
#                 continue
        
#         # Nếu đã tìm thấy ít nhất 1 element quan trọng, return True
#         if found_elements:
#             print(f"🎉 Facebook UI đã load thành công!")
#             print(f"📋 Các element đã phát hiện: {found_elements}")
#             return True
            
#         time.sleep(1)
    
#     print("❌ Facebook UI không load đầy đủ - không tìm thấy element nào")
#     return False
import uiautomator2 as u2
import logging
import subprocess
import threading
import time
from typing import Dict, List, Optional, Any
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger(__name__)

class U2DeviceManager:
    def __init__(self, max_concurrent_devices: int = 50):
        self.devices = {}  # device_id -> u2.Device
        self.device_locks = {}  # device_id -> threading.Lock
        self.connection_lock = threading.Lock()  # Lock cho việc tạo connection
        self.max_concurrent_devices = max_concurrent_devices
        self.setup_timeout = 120  # Timeout cho setup process (seconds)
        
    def connect_device(self, device_id: str, auto_setup: bool = True) -> bool:
        """Kết nối thiết bị qua U2 với auto-setup (thread-safe)"""
        # Kiểm tra đã kết nối chưa (thread-safe check)
        if device_id in self.devices:
            logger.info(f"Device {device_id} already connected")
            return True
            
        # Kiểm tra giới hạn
        if len(self.devices) >= self.max_concurrent_devices:
            logger.warning(f"Max concurrent devices reached: {self.max_concurrent_devices}")
            return False
            
        # Kết nối ADB trước nếu là emulator
        if not self._ensure_adb_connection(device_id):
            return False
            
        # Thử kết nối U2
        return self._connect_with_retry(device_id, auto_setup)
    
    def _ensure_adb_connection(self, device_id: str) -> bool:
        """Đảm bảo ADB connection cho emulator"""
        try:
            if device_id.startswith('emulator-'):
                port = device_id.split('-')[1]
                adb_device = f"127.0.0.1:{port}"
                
                # Thử kết nối ADB
                result = subprocess.run(['adb', 'connect', adb_device], 
                                      capture_output=True, text=True, timeout=15)
                
                if result.returncode == 0:
                    logger.info(f"ADB connected to {adb_device}")
                else:
                    logger.warning(f"ADB connection warning for {adb_device}: {result.stderr}")
                
                # Đợi một chút cho ADB ổn định
                time.sleep(1)
                
            return True
            
        except Exception as e:
            logger.error(f"ADB connection failed for {device_id}: {e}")
            return False
    
    def _connect_with_retry(self, device_id: str, auto_setup: bool) -> bool:
        """Kết nối U2 với retry và auto-setup"""
        try:
            # Tăng timeout lên 60 giây
            import uiautomator2 as u2
            # Set timeout
            u2.DEBUG = True  # Enable debug logs
            
            logger.info(f"Attempting direct U2 connection to {device_id}...")
            
            # Thêm timeout setting
            d = u2.connect(device_id, timeout=60)
            
            # d = u2.connect(device_id)
            
            # Test connection bằng cách lấy device info
            device_info = d.device_info
            
            # **SỬA: Lưu device và lock với connection_lock**
            with self.connection_lock:
                self.devices[device_id] = d
                self.device_locks[device_id] = threading.Lock()
            
            logger.info(f"✅ U2 connected to {device_id} (service already installed)")
            logger.info(f"   Device: {device_info.get('brand', 'Unknown')} {device_info.get('model', 'Unknown')}")
            
            return True
            
        except Exception as direct_error:
            logger.warning(f"Direct U2 connection failed for {device_id}: {direct_error}")
            
            if not auto_setup:
                logger.error(f"Auto-setup disabled, connection failed for {device_id}")
                return False
            
            # Bước 2: Auto setup U2 service
            return self._setup_u2_service(device_id)
    
    def _setup_u2_service(self, device_id: str) -> bool:
        """Cài đặt U2 service cho device"""
        try:
            logger.info(f"🔧 Setting up U2 service for {device_id}...")
            
            # Tạo connection để setup
            d = u2.connect(device_id)
            
            # Cài đặt U2 service (có thể mất vài phút)
            logger.info(f"Installing U2 service components for {device_id}...")
            d.app_install_auto()
            
            # Đợi service khởi động
            logger.info(f"Waiting for U2 service to start on {device_id}...")
            time.sleep(5)
            
            # Thử kết nối lại với timeout
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    # Test connection
                    device_info = d.device_info
                    
                    # **SỬA: Lưu device và lock với connection_lock**
                    with self.connection_lock:
                        self.devices[device_id] = d
                        self.device_locks[device_id] = threading.Lock()
                    
                    logger.info(f"✅ U2 service setup completed for {device_id}")
                    logger.info(f"   Device: {device_info.get('brand', 'Unknown')} {device_info.get('model', 'Unknown')}")
                    logger.info(f"   Android: {device_info.get('version', 'Unknown')}")
                    
                    return True
                    
                except Exception as test_error:
                    if attempt < max_retries - 1:
                        logger.warning(f"U2 service not ready for {device_id}, retrying in 3s... (attempt {attempt + 1}/{max_retries})")
                        time.sleep(3)
                    else:
                        logger.error(f"U2 service setup failed for {device_id} after {max_retries} attempts: {test_error}")
                        return False
            
            return False
            
        except Exception as setup_error:
            logger.error(f"❌ U2 service setup failed for {device_id}: {setup_error}")
            return False
    
    def get_device(self, device_id: str) -> Optional[u2.Device]:
        """Lấy U2 device instance"""
        return self.devices.get(device_id)
    
    def get_device_with_lock(self, device_id: str) -> tuple:
        """Lấy device với lock để đảm bảo thread-safe"""
        device = self.devices.get(device_id)
        lock = self.device_locks.get(device_id)
        return device, lock
    
    def connect_multiple_devices_parallel(self, device_ids: List[str], auto_setup: bool = True) -> Dict[str, bool]:
        """Kết nối nhiều thiết bị song song với auto-setup"""
        results = {}
        
        if not device_ids:
            return results
            
        # Giới hạn số worker để tránh overload hệ thống
        max_workers = min(len(device_ids), 8)
        
        logger.info(f"🔄 Connecting {len(device_ids)} devices with {max_workers} workers (auto-setup: {auto_setup})...")
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit tất cả tasks
            futures = {executor.submit(self.connect_device, device_id, auto_setup): device_id 
                      for device_id in device_ids}
            
            # Collect results với progress tracking
            completed = 0
            for future in as_completed(futures):
                device_id = futures[future]
                try:
                    results[device_id] = future.result()
                    completed += 1
                    
                    status = "✅ Success" if results[device_id] else "❌ Failed"
                    logger.info(f"[{completed}/{len(device_ids)}] {device_id}: {status}")
                    
                except Exception as e:
                    logger.error(f"Error connecting {device_id}: {e}")
                    results[device_id] = False
                    completed += 1
                    logger.info(f"[{completed}/{len(device_ids)}] {device_id}: ❌ Exception")
                    
        return results
    
    def execute_with_lock(self, device_id: str, func, *args, **kwargs) -> Dict[str, Any]:
        """Thực thi function với device lock để đảm bảo thread-safe"""
        device, lock = self.get_device_with_lock(device_id)
        
        if not device or not lock:
            return {"success": False, "error": f"Device {device_id} not connected"}
            
        with lock:
            try:
                result = func(device, *args, **kwargs)
                # Nếu function không return dict, wrap nó
                if not isinstance(result, dict):
                    return {"success": True, "result": result}
                return result
                
            except Exception as e:
                logger.error(f"Error executing function on {device_id}: {e}")
                return {"success": False, "error": str(e)}
    
    def test_device_connection(self, device_id: str) -> Dict[str, Any]:
        """Test connection và lấy thông tin device"""
        def test_func(device):
            device_info = device.device_info
            screen_info = device.window_size()
            
            return {
                "device_info": device_info,
                "screen_size": screen_info,
                "brand": device_info.get('brand', 'Unknown'),
                "model": device_info.get('model', 'Unknown'),
                "version": device_info.get('version', 'Unknown'),
                "width": screen_info[0],
                "height": screen_info[1]
            }
        
        return self.execute_with_lock(device_id, test_func)
    
    def take_screenshot(self, device_id: str, filename: str = None) -> Dict[str, Any]:
        """Chụp màn hình device"""
        def screenshot_func(device):
            if not filename:
                screenshot_name = f"screenshot_{device_id}_{int(time.time())}.png"
            else:
                screenshot_name = filename
                
            # Tạo thư mục nếu chưa có
            import os
            os.makedirs("screenshots", exist_ok=True)
            
            screenshot_path = f"screenshots/{screenshot_name}"
            device.screenshot(screenshot_path)
            
            return {
                "screenshot_path": screenshot_path,
                "filename": screenshot_name
            }
        
        return self.execute_with_lock(device_id, screenshot_func)
    
    def disconnect_device(self, device_id: str):
        """Ngắt kết nối device"""
        with self.connection_lock:
            if device_id in self.devices:
                try:
                    # Không cần đóng connection explicitly với u2
                    del self.devices[device_id]
                    if device_id in self.device_locks:
                        del self.device_locks[device_id]
                    logger.info(f"Disconnected {device_id}")
                except Exception as e:
                    logger.error(f"Error disconnecting {device_id}: {e}")
    
    def disconnect_all(self):
        """Ngắt kết nối tất cả devices"""
        device_ids = list(self.devices.keys())
        for device_id in device_ids:
            self.disconnect_device(device_id)
        logger.info("All devices disconnected")
    
    def get_connected_devices(self) -> List[str]:
        """Lấy danh sách thiết bị đã kết nối"""
        return list(self.devices.keys())
    
    def get_connection_stats(self) -> Dict[str, Any]:
        """Lấy thống kê kết nối"""
        connected_devices = self.get_connected_devices()
        device_info = {}
        
        for device_id in connected_devices:
            try:
                device = self.devices[device_id]
                info = device.device_info
                device_info[device_id] = {
                    "brand": info.get('brand', 'Unknown'),
                    "model": info.get('model', 'Unknown'),
                    "version": info.get('version', 'Unknown')
                }
            except:
                device_info[device_id] = {"status": "connection_error"}
        
        return {
            "total_connected": len(connected_devices),
            "max_concurrent": self.max_concurrent_devices,
            "connected_devices": connected_devices,
            "device_details": device_info
        }
    
    def health_check(self) -> Dict[str, Any]:
        """Kiểm tra sức khỏe tất cả connections"""
        results = {}
        
        for device_id in self.get_connected_devices():
            try:
                test_result = self.test_device_connection(device_id)
                results[device_id] = {
                    "status": "healthy" if test_result.get("success") else "unhealthy",
                    "details": test_result
                }
            except Exception as e:
                results[device_id] = {
                    "status": "error",
                    "error": str(e)
                }
        
        healthy_count = sum(1 for r in results.values() if r["status"] == "healthy")
        
        return {
            "total_devices": len(results),
            "healthy_devices": healthy_count,
            "unhealthy_devices": len(results) - healthy_count,
            "results": results
        }
    
    def __del__(self):
        """Cleanup khi manager bị destroy"""
        try:
            self.disconnect_all()
        except:
            pass
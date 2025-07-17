import threading
import logging
from typing import List, Dict, Any
from utils.u2_device_manager import U2DeviceManager

logger = logging.getLogger(__name__)

class GlobalU2Pool:
    """Singleton Pattern cho U2 Connection Pool - duy trì connections xuyên suốt app lifecycle"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Khởi tạo instance một lần duy nhất"""
        self.manager = U2DeviceManager(max_concurrent_devices=50)
        self.initialized = False
        self.connected_devices = []
        self.initialization_lock = threading.Lock()
        logger.info("🏗️ Global U2 Pool instance created")
    
    def initialize_connections(self, device_ids: List[str]) -> List[str]:
        """Khởi tạo connections một lần, các lần sau sử dụng lại"""
        with self.initialization_lock:
            if not self.initialized:
                logger.info("🔄 Initializing global U2 connection pool...")
                logger.info(f"📋 Connecting to devices: {device_ids}")
                
                # Kết nối tất cả devices
                results = self.manager.connect_multiple_devices_parallel(device_ids)
                
                # Lấy devices kết nối thành công
                connected = [device_id for device_id in device_ids if results.get(device_id, False)]
                failed = [device_id for device_id in device_ids if not results.get(device_id, False)]
                
                # Lưu trạng thái
                self.connected_devices = connected
                self.initialized = True
                
                logger.info(f"✅ Global U2 pool initialized")
                logger.info(f"  📊 Connected: {len(connected)}/{len(device_ids)} devices")
                logger.info(f"  🔗 Devices: {connected}")
                
                if failed:
                    logger.warning(f"  ❌ Failed: {failed}")
                
                return connected
            else:
                logger.info("🔄 Using existing U2 connection pool...")
                logger.info(f"  📊 Available devices: {len(self.connected_devices)}")
                logger.info(f"  🔗 Devices: {self.connected_devices}")
                
                # Kiểm tra health của existing connections
                healthy_devices = self._health_check()
                
                if len(healthy_devices) < len(self.connected_devices):
                    logger.warning(f"⚠️ Some connections unhealthy: {len(healthy_devices)}/{len(self.connected_devices)}")
                
                return healthy_devices
    
    def _health_check(self) -> List[str]:
        """Kiểm tra sức khỏe connections"""
        healthy = []
        
        for device_id in self.connected_devices:
            try:
                device = self.manager.get_device(device_id)
                if device:
                    # Test connection nhanh
                    _ = device.device_info
                    healthy.append(device_id)
            except Exception as e:
                logger.warning(f"Device {device_id} unhealthy: {e}")
        
        return healthy
    
    def get_manager(self) -> U2DeviceManager:
        """Lấy U2 manager instance"""
        return self.manager
    
    def get_connected_devices(self) -> List[str]:
        """Lấy danh sách devices đã kết nối"""
        return self.connected_devices.copy()
    
    def get_connection_stats(self) -> Dict[str, Any]:
        """Lấy thống kê connection pool"""
        stats = self.manager.get_connection_stats()
        stats.update({
            "pool_initialized": self.initialized,
            "pool_devices": self.connected_devices,
            "pool_device_count": len(self.connected_devices)
        })
        return stats
    
    def is_initialized(self) -> bool:
        """Kiểm tra pool đã khởi tạo chưa"""
        return self.initialized
    
    def reset_pool(self):
        """Reset pool - dùng khi cần reconnect tất cả"""
        with self.initialization_lock:
            logger.info("🔄 Resetting global U2 pool...")
            self.manager.disconnect_all()
            self.initialized = False
            self.connected_devices = []
            # Tạo manager mới
            self.manager = U2DeviceManager(max_concurrent_devices=50)
            logger.info("✅ Global U2 pool reset completed")
    
    def cleanup(self):
        """Cleanup khi app đóng"""
        with self.initialization_lock:
            if hasattr(self, 'manager') and self.initialized:
                logger.info("🧹 Cleaning up global U2 pool...")
                self.manager.disconnect_all()
                self.initialized = False
                self.connected_devices = []
                logger.info("✅ Global U2 pool cleaned up")
    
    def __del__(self):
        """Destructor - cleanup cuối cùng"""
        try:
            self.cleanup()
        except:
            pass

# **Global instance - import này để sử dụng**
global_u2_pool = GlobalU2Pool()
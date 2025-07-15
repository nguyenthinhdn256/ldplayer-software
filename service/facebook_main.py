# facebook_main.py
import logging
import threading
import subprocess
import sys, os, json
from typing import Dict, Any

logger = logging.getLogger(__name__)

class FacebookRegistrationStarter:
    """Class chỉ để gọi worker, không xử lý logic registration"""
    
    def __init__(self, parent_window=None):
        self.parent_window = parent_window
        self.registration_config = {}
        
    def call_worker_only(self):
        """Chỉ gọi worker và dừng lại, không làm gì khác"""
        try:
            # Thu thập cấu hình cơ bản
            self.registration_config = self.collect_basic_configuration()
            threading.Thread(target=self._call_worker_thread, args=(self.registration_config,), daemon=True).start()
            return True
            
        except Exception as e:
            logger.error(f"Error calling worker: {e}")
            return False
    
    def collect_basic_configuration(self) -> Dict[str, Any]:
        """Thu thập cấu hình cơ bản cần thiết cho worker"""
        config = {}
        
        try:
            # Tìm groupbox4_manager
            app_window = self.parent_window
            while app_window and not hasattr(app_window, 'groupbox4_manager'):
                app_window = app_window.master if hasattr(app_window, 'master') else None
                
            if app_window and hasattr(app_window, 'groupbox4_manager'):
                groupbox4_manager = app_window.groupbox4_manager
                
                # Lấy số LD/Phone
                if hasattr(groupbox4_manager, 'groupbox3_manager'):
                    config['so_ld'] = int(groupbox4_manager.groupbox3_manager.so_ld_var.get())
                
                # Lấy danh sách devices đã chọn
                if hasattr(groupbox4_manager, 'ldgroupbox1_manager'):
                    selected_devices = []
                    device_manager = groupbox4_manager.ldgroupbox1_manager
                    if hasattr(device_manager, 'device_checkboxes'):
                        selected_devices = [device_id for device_id, checkbox_var in device_manager.device_checkboxes.items() if checkbox_var.get()]
                    config['selected_devices'] = selected_devices
            
            logger.info(f"Collected basic config: {config}")
            return config
            
        except Exception as e:
            logger.error(f"Error collecting config: {e}")
            return {}
    
    def _call_worker_thread(self, config: Dict[str, Any]):
        """Thread để gọi worker - chạy trực tiếp, không qua subprocess"""
        try:
            logger.info("Starting facebook_registration_worker directly...")
            from service.facebook_registration_worker import FacebookRegistrationWorker
            # Tạo worker instance
            worker = FacebookRegistrationWorker(max_workers=4)
            # Khởi tạo worker pool
            init_result = worker.initialize_worker_pool(config)
            
            if init_result.get('success', False):
                logger.info("Worker pool initialized successfully")
                
                # Chạy main logic - sẽ chạy liên tục
                final_result = worker.main(config)
                logger.info(f"Worker result: {final_result}")
            else:
                logger.error(f"Worker initialization failed: {init_result}")
                
        except Exception as e:
            logger.error(f"Error in worker thread: {e}")

def start_facebook_registration(parent_window):
    """Hàm tiện ích - giờ chỉ gọi worker"""
    try:
        starter = FacebookRegistrationStarter(parent_window)
        return starter.call_worker_only()
        
    except Exception as e:
        logger.error(f"Error starting worker: {e}")
        return False

if __name__ == "__main__":
    print("Facebook Registration Starter - Worker caller only")
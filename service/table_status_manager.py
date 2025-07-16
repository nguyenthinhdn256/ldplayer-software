import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class TableStatusManager:
    def __init__(self):
        self.table_status_templates = {}
        self.setup_table_status_templates()
    
    def setup_table_status_templates(self):
        """Thiết lập các template status cho table với đầy đủ 12 field"""
        self.table_status_templates = {
            "starting_status": {"stt": "", "trang_thai": "Đã đổi ngôn ngữ sang tiếng Việt", "ten_may": "", "ket_qua": "", "ho": "", "ten": "", "mat_khau": "", "email_sdt": "", "uid": "", "cookie": "", "token": "", "proxy": ""},
            "start_change_language": {"stt": "", "trang_thai": "Bắt đầu đổi ngôn ngữ sang tiếng Việt", "ten_may": "", "ket_qua": "", "ho": "", "ten": "", "mat_khau": "", "email_sdt": "", "uid": "", "cookie": "", "token": "", "proxy": ""},
            "done_change_language": {"stt": "", "trang_thai": "Đã đổi ngôn ngữ sang tiếng Việt", "ten_may": "", "ket_qua": "", "ho": "", "ten": "", "mat_khau": "", "email_sdt": "", "uid": "", "cookie": "", "token": "", "proxy": ""}
        }
        logger.info(f"Đã thiết lập {len(self.table_status_templates)} template status")
    
    def update_device_status(self, device_index: int, status_data: Dict[str, str], table_manager=None):
        """Cập nhật status cho một device với đầy đủ 12 field"""
        try:
            # Đảm bảo có đầy đủ 12 field
            required_fields = ["stt", "trang_thai", "ten_may", "ket_qua", "ho", "ten", "mat_khau", "email_sdt", "uid", "cookie", "token", "proxy"]
            for field in required_fields:
                if field not in status_data:
                    status_data[field] = ""
            
            # # Tự động set stt nếu trống
            # if not status_data["stt"]:
            #     status_data["stt"] = str(device_index + 1)
            logger.info(f"Updating device_index={device_index}, STT={status_data['stt']}, Status={status_data['trang_thai']}")
            
            # GỌI UPDATE TABLE UI THREAD-SAFE
            if table_manager and hasattr(table_manager, 'update_table_row_safe'):
                table_manager.update_table_row_safe(device_index, status_data)
            elif table_manager and hasattr(table_manager, 'update_table_row'):
                # Fallback cho old method
                table_manager.update_table_row(device_index, status_data)
            
            logger.info(f"Cập nhật status cho device {device_index + 1}: {status_data['trang_thai']}")
            return True
            
        except Exception as e:
            logger.error(f"Lỗi khi cập nhật status device {device_index}: {str(e)}")
            return False
    
    def update_devices_status_batch(self, devices_status_list: List[Dict[str, str]], table_manager=None):
        """Cập nhật status cho nhiều devices cùng lúc với đầy đủ 12 field mỗi device"""
        try:
            for i, status_data in enumerate(devices_status_list):
                self.update_device_status(i, status_data, table_manager)
            
            logger.info(f"Cập nhật batch status cho {len(devices_status_list)} devices")
            return True
            
        except Exception as e:
            logger.error(f"Lỗi khi cập nhật batch status: {str(e)}")
            return False
    
    def get_template(self, template_name: str) -> Dict[str, str]:
        """Lấy template theo tên"""
        return self.table_status_templates.get(template_name, {})
    
    def get_all_templates(self) -> Dict[str, Dict[str, str]]:
        """Lấy tất cả templates"""
        return self.table_status_templates
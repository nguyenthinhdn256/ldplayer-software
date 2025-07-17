# service/facebook_registration_worker.py
import argparse
import json
import logging
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from service.facebook_funtion_manager import XuLyBuoc1
from service.table_status_manager import TableStatusManager
from utils.u2_device_manager import U2DeviceManager
from utils.global_u2_pool import global_u2_pool
from typing import Dict, Any

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FacebookRegistrationWorker:
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.executor = None
        self.device_ids = []
        self.status_manager = TableStatusManager()
        self.u2_manager = global_u2_pool.get_manager()
        logger.info(f"Initializing FacebookRegistrationWorker with {max_workers} workers")
    
    def initialize_worker_pool(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Tạo worker pool với số workers = số devices"""
        try:
            logger.info("Creating unlimited worker pool...")
            
            # Lấy cấu hình
            original_device_ids = config.get('selected_devices', [])
            self.table_manager = config.get('table_manager')
            so_ld = config.get('so_ld', 1)
            
            # **SỬA: Sử dụng selected_devices, chỉ tạo mock khi thực sự trống**
            if not original_device_ids or len(original_device_ids) == 0:
                original_device_ids = [f"mock_device_{i+1}" for i in range(so_ld)]
                logger.info(f"Created mock devices: {original_device_ids}")
            else:
                logger.info(f"Using selected devices: {original_device_ids}")

            # **THÊM: Sắp xếp device_ids theo thứ tự port từ thấp đến cao**
            def get_port_number(device_id):
                """Lấy port number từ device_id để sắp xếp"""
                if device_id.startswith('emulator-'):
                    try:
                        return int(device_id.split('-')[1])
                    except:
                        return 99999  # fallback cho device không đúng format
                else:
                    return 0  # device thật sẽ đứng đầu
            
            # Sắp xếp devices theo port
            sorted_device_ids = sorted(original_device_ids, key=get_port_number)
            logger.info(f"📋 Sorted devices: {sorted_device_ids}")

             # **BƯỚC QUAN TRỌNG: Kết nối tất cả devices qua U2 song song**
            logger.info(f"Connecting {len(self.device_ids)} devices via U2...")
            connected_devices = global_u2_pool.initialize_connections(sorted_device_ids)
            
            failed_devices = [device_id for device_id in sorted_device_ids if device_id not in connected_devices]
            
            # **QUAN TRỌNG: Giữ thứ tự đã sắp xếp**
            logger.info(f"📊 Connected devices in order: {connected_devices}")


            # Log kết quả
            logger.info(f"U2 Connection Results:")
            logger.info(f"  ✅ Connected: {len(connected_devices)}/{len(self.device_ids)}")
            logger.info(f"  ❌ Failed: {len(failed_devices)}")
            
            if failed_devices:
                logger.warning(f"Failed devices: {failed_devices}")
            
            if not connected_devices:
                return {'success': False, 'error': 'No devices connected via U2', 'failed_devices': failed_devices}
            
            # Cập nhật device_ids chỉ với những devices kết nối thành công
            self.device_ids = connected_devices


            # Tạo ThreadPoolExecutor với max_workers = số devices
            num_workers = len(connected_devices)
            self.executor = ThreadPoolExecutor(max_workers=num_workers)
            
            # Log thống kê U2
            stats = self.u2_manager.get_connection_stats()
            logger.info(f"U2 Connection Stats: {stats}")
            
            logger.info(f"✅ Worker pool initialized with {num_workers} workers for U2 devices")
            logger.info("🛑 U2 connections ready. Ready for task execution.")
            
            return {'success': True, 'message': f'U2 worker pool initialized with {num_workers} devices', 'workers': num_workers, 'connected_devices': connected_devices, 'failed_devices': failed_devices, 'u2_stats': stats, 'status': 'ready_for_execution'}
            
        except Exception as e:
            logger.error(f"❌ Error initializing worker pool: {e}")
            return {'success': False, 'error': str(e)}

    def main(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Main function để xử lý logic registration"""
        try:
            logger.info("🚀 Starting main registration logic...")
            
            # Bước 1: Sleep 10 giây trước
            logger.info("Step 1: Tạm nghỉ 5s lần 1")
            time.sleep(5)
            
            # Bước 2: Khởi tạo worker đa tiến trình xử lý song song (sau sleep)
            logger.info("Step 2: Initializing parallel workers...")
            futures = []
            for i, device_id in enumerate(self.device_ids):
                # i sẽ tương ứng với row index trong bảng
                future = self.executor.submit(self.process_device, device_id, i)
                futures.append(future)
                logger.info(f"🚀 Submitted PARALLEL task {i+1} for device {device_id} -> row {i+1}")
        
            logger.info(f"📋 Total {len(futures)} tasks submitted for PARALLEL execution")    
            # Dừng code tại đây
            logger.info("🛑 Code stopped here as requested")
            
            return {'success': True, 'message': 'U2 workers initialized and running', 'active_workers': len(futures), 'devices': self.device_ids}

        except Exception as e:
            logger.error(f"❌ Error in main registration logic: {e}")
            return {'success': False, 'error': str(e)}
        
        finally:
            # Cleanup
            pass

    def process_device(self, device_id: str, device_index: int):
        try:
            
            stt_display = str(device_index + 1)

            # **BƯỚC 1: Kiểm tra kết nối U2**
            logger.info(f"Processing device {device_id} with U2...")

            # Lấy U2 device instance
            u2_device = self.u2_manager.get_device(device_id)

            if not u2_device: 
                error_status = {"stt": stt_display, "trang_thai": "Global U2 Pool: Device not found", "ten_may": device_id, "ket_qua": "", "ho": "", "ten": "", "mat_khau": "", "email_sdt": "", "uid": "", "cookie": "", "token": "", "proxy": ""}
                self.status_manager.update_device_status(device_index, error_status, self.table_manager)
                return f"Error: U2 device not found for {device_id}"

            def test_u2_connection(device):
                """Test function để chạy với lock"""
                device_info = device.device_info
                return {"success": True, "brand": device_info.get('brand', 'Unknown'), "model": device_info.get('model', 'Unknown'), "version": device_info.get('version', 'Unknown')}

            # Thực thi test với lock
            test_result = self.u2_manager.execute_with_lock(device_id, test_u2_connection)
            
            if test_result.get("success"):
                # U2 connection OK
                device_info = test_result
                u2_ready_status = {"stt": stt_display, "trang_thai": f"Global U2 Pool Ready - {device_info.get('brand', 'Unknown')} {device_info.get('model', 'Unknown')}", "ten_may": device_id, "ket_qua": "", "ho": "", "ten": "", "mat_khau": "", "email_sdt": "", "uid": "", "cookie": "", "token": "", "proxy": ""}
                self.status_manager.update_device_status(device_index, u2_ready_status, self.table_manager)
                logger.info(f"✅ U2 ready for {device_id}: {device_info.get('brand', 'Unknown')} {device_info.get('model', 'Unknown')}")
            else:
                error_status = {"stt": stt_display, "trang_thai": f"Global U2 Pool Error: {test_result.get('error', 'Unknown')}", "ten_may": device_id, "ket_qua": "", "ho": "", "ten": "", "mat_khau": "", "email_sdt": "", "uid": "", "cookie": "", "token": "", "proxy": ""}
                self.status_manager.update_device_status(device_index, error_status, self.table_manager)
                return f"U2 Error for {device_id}: {test_result.get('error', 'Unknown')}"
            

            time.sleep(1)
            logger.info("Step 1: Tạm nghỉ 5s lần 2")
            time.sleep(5)


            # Thực hiện thây đổi ngôn ngữ.
            start_change_language_status = {"stt": stt_display, "trang_thai": "Bắt đầu đổi ngôn ngữ sang tiếng Việt", "ten_may": device_id, "ket_qua": "", "ho": "", "ten": "", "mat_khau": "", "email_sdt": "", "uid": "", "cookie": "", "token": "", "proxy": ""}    
            self.status_manager.update_device_status(device_index, start_change_language_status, self.table_manager)
            xu_ly_buoc1 = XuLyBuoc1(device_id)
            language_result = xu_ly_buoc1.thay_doi_ngon_ngu()
            
            time.sleep(5)
            done_change_language_status = {"stt": stt_display, "trang_thai": "Đã đổi ngôn ngữ sang tiếng Việt", "ten_may": device_id, "ket_qua": "", "ho": "", "ten": "", "mat_khau": "", "email_sdt": "", "uid": "", "cookie": "", "token": "", "proxy": ""}
            self.status_manager.update_device_status(device_index, done_change_language_status, self.table_manager)

            return f"Processed {device_id}"

        except Exception as e:
            logger.error(f"Error processing device {device_id}: {e}")
            error_status = {"stt": stt_display, "trang_thai": f"Lỗi: {str(e)}", "ten_may": device_id, "ket_qua": "Lỗi", "ho": "", "ten": "", "mat_khau": "", "email_sdt": "", "uid": "", "cookie": "", "token": "", "proxy": ""}
            self.status_manager.update_device_status(device_index, error_status, self.table_manager)
            return f"Error processing {device_id}: {e}"

    def __del__(self):
        """Cleanup khi worker bị destroy"""
        if hasattr(self, 'executor') and self.executor:
            self.executor.shutdown(wait=False)
        logger.info("Worker cleaned up (Global U2 Pool connections preserved)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Facebook Registration Worker')
    parser.add_argument('--config', required=True, help='Configuration file path')
    parser.add_argument('--workers', type=int, default=4, help='Number of workers')
    args = parser.parse_args()

    try:
        # Load config
        with open(args.config, 'r', encoding='utf-8') as f:
            config = json.load(f)
        logger.info("🚀 Starting Facebook Registration Worker...")
        worker = FacebookRegistrationWorker(max_workers=args.workers)
        init_result = worker.initialize_worker_pool(config)
        
        if init_result.get('success', False):
            final_result = worker.main(config)
            print(json.dumps(final_result, ensure_ascii=False, indent=2))
            sys.exit(0 if final_result.get('success', False) else 1)
        else:
            print(json.dumps(init_result, ensure_ascii=False, indent=2))
            sys.exit(1)
        
    except Exception as e:
        error_result = {'success': False, 'error': str(e)}
        print(json.dumps(error_result))
        logger.error(f"❌ Worker failed: {e}")
        sys.exit(1)
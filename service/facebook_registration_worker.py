# service/facebook_registration_worker.py
import argparse
import json
import logging
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from service.facebook_funtion_manager import XuLyBuoc1
from typing import Dict, Any

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FacebookRegistrationWorker:
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.executor = None
        self.device_ids = []
        logger.info(f"Initializing FacebookRegistrationWorker with {max_workers} workers")
    
    def initialize_worker_pool(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Tạo worker pool và chuẩn bị device list"""
        try:
            logger.info("Creating worker pool...")
            
            # Tạo ThreadPoolExecutor
            self.executor = ThreadPoolExecutor(max_workers=self.max_workers)
            logger.info(f"✅ Worker pool created with {self.max_workers} workers")
            
            # Lấy danh sách devices
            self.device_ids = config.get('selected_devices', [])
            so_ld = config.get('so_ld', 1)
            
            # Nếu không có devices, tạo mock devices
            if not self.device_ids:
                self.device_ids = [f"mock_device_{i+1}" for i in range(so_ld)]
            
            logger.info(f"✅ Prepared {len(self.device_ids)} devices")
            logger.info("🛑 Worker initialization completed. Ready for task execution.")
            
            return {'success': True, 'message': 'Worker pool initialized successfully', 'workers': self.max_workers, 'devices_prepared': len(self.device_ids), 'status': 'ready_for_execution'}
            
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
                future = self.executor.submit(self.process_device, device_id, i+1)
                futures.append(future)
                logger.info(f"Submitted task {i+1} for device {device_id}")
            
            # Dừng code tại đây
            logger.info("🛑 Code stopped here as requested")
            
            return {'success': True, 'message': 'Code execution completed'}
            
        except Exception as e:
            logger.error(f"❌ Error in main registration logic: {e}")
            return {'success': False, 'error': str(e)}
        
        finally:
            # Cleanup
            if self.executor:
                self.executor.shutdown(wait=True)
                logger.info("Worker pool shutdown completed")

    def process_device(self, device_id: str, task_id: int):
        """Function để xử lý từng device (chạy trong worker thread)"""
        logger.info(f"Worker thread processing device {device_id} (task {task_id})")
        time.sleep(1)
        logger.info("Step 1: Tạm nghỉ 5s lần 2")
        time.sleep(5)

        # Thực hiện thây đổi ngôn ngữ.
        xu_ly_buoc1 = XuLyBuoc1(device_id)
        language_result = xu_ly_buoc1.thay_doi_ngon_ngu()
        time.sleep(15)
        logger.info(f"Đã thây đổi ngôn ngữ sang: {language_result}")
        return f"Processed {device_id}"

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
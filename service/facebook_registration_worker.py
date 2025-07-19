# service/facebook_registration_worker.py
import argparse
import json
import logging
import sys
import time, random
import uiautomator2 as u2 
from concurrent.futures import ThreadPoolExecutor
from service.facebook_funtion_manager import XuLyBuoc1
from service.table_status_manager import TableStatusManager
from service.moi_data_manager import MailTheoTepHandler, SDTTheoTepHandler, MailDuoiMailHandler, SDTDauSoHandler
from service.facebook_funtion_manager import XuLyBuoc1, get_password_configuration
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
        self.moi_config = None
        logger.info(f"Initializing FacebookRegistrationWorker with {max_workers} workers")
    
    def initialize_worker_pool(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Tạo worker pool với số workers = số devices"""
        try:
            logger.info("Creating unlimited worker pool...")
            # **THÊM DEBUG LOG**
            logger.info(f"🔍 DEBUG - Received config: {config}")
            
            # Lấy cấu hình
            original_device_ids = config.get('selected_devices', [])
            logger.info(f"🔍 DEBUG - original_device_ids from config: {original_device_ids}")

            self.table_manager = config.get('table_manager')
            so_ld = config.get('so_ld', 1)
            self.moi_config = config.get('moi_config')
            
            # **KIỂM TRA DEVICES THỰC TẾ QUA ADB**
            logger.info("Checking real ADB devices...")
            try:
                import subprocess
                result = subprocess.run(['adb', 'devices'], capture_output=True, text=True, timeout=10)
                adb_devices = []
                for line in result.stdout.strip().split('\n')[1:]:
                    if line.strip() and '\t' in line:
                        device_id, status = line.strip().split('\t')
                        if status == 'device':
                            adb_devices.append(device_id)
                logger.info(f"📱 ADB devices online: {adb_devices}")
            except Exception as e:
                logger.error(f"❌ Error checking ADB devices: {e}")
                return {'success': False, 'error': f'ADB check failed: {str(e)}'}
            
            # **VALIDATION DEVICES**
            if not original_device_ids or len(original_device_ids) == 0:
                logger.error("❌ No devices selected from GUI")
                return {'success': False, 'error': 'No devices selected', 'message': 'Vui lòng chọn devices từ tab QUẢN LÝ LD/PHONE trước khi Start'}
            
            # Lọc chỉ những devices thực sự online
            valid_devices = [device_id for device_id in original_device_ids if device_id in adb_devices]
            
            if not valid_devices:
                logger.error(f"❌ No valid devices found. Selected: {original_device_ids}, Online: {adb_devices}")
                return {'success': False, 'error': 'No valid devices online', 'message': f'Devices được chọn không online. Có sẵn: {adb_devices}. Đã chọn: {original_device_ids}'}
            
            # **SẮPXẾP DEVICES THEO PORT**
            def get_port_number(device_id):
                if device_id.startswith('emulator-'):
                    try:
                        return int(device_id.split('-')[1])
                    except:
                        return 99999
                else:
                    return 0
            
            sorted_device_ids = sorted(valid_devices, key=get_port_number)
            logger.info(f"📋 Sorted valid devices: {sorted_device_ids}")
            
            # **KẾT NỐI TẤT CẢ DEVICES QUA U2 SONG SONG**
            logger.info(f"Connecting {len(sorted_device_ids)} devices via U2...")
            connected_devices = global_u2_pool.initialize_connections(sorted_device_ids)
            
            failed_devices = [device_id for device_id in sorted_device_ids if device_id not in connected_devices]
            
            # Log kết quả
            logger.info(f"U2 Connection Results:")
            logger.info(f"  ✅ Connected: {len(connected_devices)}/{len(sorted_device_ids)}")
            logger.info(f"  ❌ Failed: {len(failed_devices)}")
            
            if failed_devices:
                logger.warning(f"Failed devices: {failed_devices}")
            
            if not connected_devices:
                return {'success': False, 'error': 'No devices connected via U2', 'failed_devices': failed_devices, 'message': 'Không có device nào kết nối U2 thành công'}
            
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
            d = u2.connect(device_id)

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
            time.sleep(3)
            done_change_language_status = {"stt": stt_display, "trang_thai": "Đã đổi ngôn ngữ sang tiếng Việt", "ten_may": device_id, "ket_qua": "", "ho": "", "ten": "", "mat_khau": "", "email_sdt": "", "uid": "", "cookie": "", "token": "", "proxy": ""}
            self.status_manager.update_device_status(device_index, done_change_language_status, self.table_manager)

            # # Change info device
            # maxchanger_start_status = {"stt": stt_display, "trang_thai": "Đang khởi động MaxChanger", "ten_may": device_id, "ket_qua": "", "ho": "", "ten": "", "mat_khau": "", "email_sdt": "", "uid": "", "cookie": "", "token": "", "proxy": ""}
            # self.status_manager.update_device_status(device_index, maxchanger_start_status, self.table_manager)
            # d.app_start('com.minsoftware.maxchanger')
            # time.sleep(5)
            # d.swipe(270, 800, 270, 200)
            # time.sleep(1)
            # d(text="CHANGE INFO").click()
            # time.sleep(5)
            # d.app_stop('com.minsoftware.maxchanger')
            # maxchanger_done_status = {"stt": stt_display, "trang_thai": "Đã thực hiện MaxChanger thành công", "ten_may": device_id, "ket_qua": "Thành công", "ho": "", "ten": "", "mat_khau": "", "email_sdt": "", "uid": "", "cookie": "", "token": "", "proxy": ""}
            # self.status_manager.update_device_status(device_index, maxchanger_done_status, self.table_manager)

            # # Tắt vị trí
            # tabvitri_start_status = {"stt": stt_display, "trang_thai": "Đang khởi động tab Vị trí", "ten_may": device_id, "ket_qua": "", "ho": "", "ten": "", "mat_khau": "", "email_sdt": "", "uid": "", "cookie": "", "token": "", "proxy": ""}
            # self.status_manager.update_device_status(device_index, tabvitri_start_status, self.table_manager)
            # d.app_start('com.android.settings', activity='.Settings$LocationSettingsActivity')
            # time.sleep(2)
            # location_switch = d(resourceId="com.android.settings:id/switch_widget")
            # if location_switch.exists and location_switch.info.get('checked', False):
            #     location_switch.click()
            # time.sleep(2)
            # d.app_stop('com.android.settings')
            # tabvitri_done_status = {"stt": stt_display, "trang_thai": "Đã tắt Vị trí", "ten_may": device_id, "ket_qua": "", "ho": "", "ten": "", "mat_khau": "", "email_sdt": "", "uid": "", "cookie": "", "token": "", "proxy": ""}
            # self.status_manager.update_device_status(device_index, tabvitri_done_status, self.table_manager)


            # Clear data và cấp quyền storage
            time.sleep(2)
            clear_start_status = {"stt": stt_display, "trang_thai": "Đang clear data và cấp quyền storage", "ten_may": device_id, "ket_qua": "", "ho": "", "ten": "", "mat_khau": "", "email_sdt": "", "uid": "", "cookie": "", "token": "", "proxy": ""}
            self.status_manager.update_device_status(device_index, clear_start_status, self.table_manager)
            
            clear_result = xu_ly_buoc1.clear_and_capquyen_app(["com.facebook.katana", "com.facebook.orca", "com.android.chrome"])
            
            if clear_result.get("success"):
                clear_done_status = {"stt": stt_display, "trang_thai": "Đã clear data và cấp quyền storage thành công", "ten_may": device_id, "ket_qua": "", "ho": "", "ten": "", "mat_khau": "", "email_sdt": "", "uid": "", "cookie": "", "token": "", "proxy": ""}
            else:
                clear_done_status = {"stt": stt_display, "trang_thai": f"Clear data thất bại: {clear_result.get('message', '')}", "ten_may": device_id, "ket_qua": "", "ho": "", "ten": "", "mat_khau": "", "email_sdt": "", "uid": "", "cookie": "", "token": "", "proxy": ""}
            
            self.status_manager.update_device_status(device_index, clear_done_status, self.table_manager)
            time.sleep(2)

            # Tiến hành reg account với vòng lặp 3 lần
            for fb_attempt in range(3):
                logger.info(f"Facebook startup attempt {fb_attempt + 1}/3")
                
                time.sleep(2)
                openfbapp_start_status = {"stt": stt_display, "trang_thai": f"Đang khởi động Facebook App - lần {fb_attempt + 1}", "ten_may": device_id, "ket_qua": "", "ho": "", "ten": "", "mat_khau": "", "email_sdt": "", "uid": "", "cookie": "", "token": "", "proxy": ""}
                self.status_manager.update_device_status(device_index, openfbapp_start_status, self.table_manager)
                d.app_start('com.facebook.katana')
                wait_facebook_result = xu_ly_buoc1.wait_facebook_app()
                time.sleep(10)
                openfbapp_done_status = {"stt": stt_display, "trang_thai": f"Đã khởi động Facebook thành công - lần {fb_attempt + 1}", "ten_may": device_id, "ket_qua": "", "ho": "", "ten": "", "mat_khau": "", "email_sdt": "", "uid": "", "cookie": "", "token": "", "proxy": ""}
                self.status_manager.update_device_status(device_index, openfbapp_done_status, self.table_manager)

                time.sleep(2)
                if d.xpath('//*[@content-desc="Meta logo" or @content-desc="Logo Meta"]').exists:
                    print(f"Đã thấy Logo Facebook - lần {fb_attempt + 1}")
                    time.sleep(1)
                    d.xpath('//*[@text="Create new account"] | //android.view.ViewGroup[3]/android.widget.Button[1] | //*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[2]/android.widget.FrameLayout[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.widget.Button[1]').click()
                    if d(text="CHO PHÉP").wait(timeout=5) or d(text="Bạn tên gì?").wait(timeout=5):
                        break
                if d.xpath('//*[@text="Hãy tạo tài khoản để kết nối với bạn bè, người thân và cộng đồng có chung sở thích."]').wait(timeout=15):
                    print(f"Đã thấy Hãy Tạo Tài Khoản - lần {fb_attempt + 1}")
                    time.sleep(1)
                    d.xpath("//android.view.ViewGroup[1]/android.widget.Button[1]").click()
                    if d(text="CHO PHÉP").wait(timeout=5) or d(text="Bạn tên gì?").wait(timeout=5):
                        break
                
                logger.warning(f"Facebook khởi động thất bại - lần {fb_attempt + 1}")
                d.app_stop('com.facebook.katana')
                time.sleep(2)
            else:
                return f"Facebook startup failed after 3 attempts for {device_id}"

            # Tiếp tục logic sau khi Facebook khởi động thành công
            if d(text="CHO PHÉP").wait(timeout=5):
                time.sleep(1) 
                d(text="CHO PHÉP").click()
           
            for attempt in range(3):
                logger.info(f"Họ tên attempt {attempt + 1}/3")
                
                # Gõ text vào field
                if d(text="Bạn tên gì?").wait(timeout=5):
                    # Lấy random họ tên mới cho mỗi lần thử
                    with open('dulieu/hoten/Ho.txt', 'r', encoding='utf-8') as f:
                        ho_list = [line.strip() for line in f.readlines() if line.strip() and not line.startswith('#')]
                        random_ho = random.choice(ho_list)
                    with open('dulieu/hoten/Ten.txt', 'r', encoding='utf-8') as f:
                        ten_list = [line.strip() for line in f.readlines() if line.strip() and not line.startswith('#')]
                        random_ten = random.choice(ten_list)
                    print(f"Bạn tên gì? - lần {attempt + 1}")
                    time.sleep(1)
                    d(text="Họ").click()
                    time.sleep(1)
                    d.send_keys(random_ho)
                    time.sleep(1)
                    d(text="Tên").click()
                    time.sleep(1)
                    d.send_keys(random_ten)
                    time.sleep(1)
                    d.xpath('//*[@text="Tiếp"]').click()
                    time.sleep(5)
                
                if d(text="Bạn tên gì?").wait(timeout=5):
                    # Lấy random họ tên mới cho mỗi lần thử
                    with open('dulieu/hoten/Ho.txt', 'r', encoding='utf-8') as f:
                        ho_list = [line.strip() for line in f.readlines() if line.strip() and not line.startswith('#')]
                        random_ho = random.choice(ho_list)
                    with open('dulieu/hoten/Ten.txt', 'r', encoding='utf-8') as f:
                        ten_list = [line.strip() for line in f.readlines() if line.strip() and not line.startswith('#')]
                        random_ten = random.choice(ten_list)
                    print(f"Bạn tên gì? vẫn xuất hiện - lần {attempt + 1}")
                    time.sleep(1)
                    d(text="Họ").click()
                    time.sleep(0.5)
                    d(description="Xóa văn bản Họ").click()
                    d.send_keys(random_ho)
                    time.sleep(1)
                    d(text="Tên").click()
                    time.sleep(0.5)
                    d(description="Xóa văn bản Tên").click()
                    time.sleep(1)
                    d.send_keys(random_ten)
                    time.sleep(1)
                    d.xpath('//*[@text="Tiếp"]').click()
                    time.sleep(5)

                if d.xpath('//*[@text="Chọn tên của bạn"]').wait(timeout=5):
                    time.sleep(1)
                    d.xpath('//*[@text="Sử dụng tên khác"]').click()
                    time.sleep(2)
                    if d(text="Bạn tên gì?").wait(timeout=5):
                        # Lấy random họ tên mới cho mỗi lần thử
                        with open('dulieu/hoten/Ho.txt', 'r', encoding='utf-8') as f:
                            ho_list = [line.strip() for line in f.readlines() if line.strip() and not line.startswith('#')]
                            random_ho = random.choice(ho_list)
                        with open('dulieu/hoten/Ten.txt', 'r', encoding='utf-8') as f:
                            ten_list = [line.strip() for line in f.readlines() if line.strip() and not line.startswith('#')]
                            random_ten = random.choice(ten_list)
                        print(f"Bạn tên gì? trong chọn tên - lần {attempt + 1}")
                        time.sleep(1)
                        d(text="Họ").click()
                        time.sleep(1)
                        d.send_keys(random_ho)
                        time.sleep(1)
                        d(text="Tên").click()
                        time.sleep(1)
                        d.send_keys(random_ten)
                        time.sleep(1)
                        d.xpath('//*[@text="Tiếp"]').click()
                        time.sleep(1)
                
                # Kiểm tra xem đã qua được bước họ tên chưa
                if not d(text="Bạn tên gì?").exists and not d.xpath('//*[@text="Chọn tên của bạn"]').exists:
                    logger.info(f"Họ tên thành công ở lần thử {attempt + 1}")
                    break
                elif attempt == 2:
                    logger.warning("Đã thử 3 lần nhập họ tên nhưng vẫn không thành công")

            hoten_done_status = {"stt": stt_display, "trang_thai": "Đã nhập Họ Tên", "ten_may": device_id, "ket_qua": "", "ho": random_ho, "ten": random_ten, "mat_khau": "", "email_sdt": "", "uid": "", "cookie": "", "token": "", "proxy": ""}
            self.status_manager.update_device_status(device_index, hoten_done_status, self.table_manager)
            #####

            if d.xpath('//*[@resource-id="android:id/button1"]').wait(timeout=5):
                print("Button SET xuất hiện")
                time.sleep(1)
                d.xpath('//*[@resource-id="android:id/button1"]').click()

            
            if d.xpath('//*[@text="Ngày sinh của bạn là khi nào?"]').wait(timeout=5):
                print("Ngày sinh của bạn là khi nào?")
                time.sleep(1)
                d.xpath('//*[@text="Tiếp"]').click()
                time.sleep(1)
                d.xpath('//*[@text="Tiếp"]').click()
                time.sleep(3)
                age = random.randint(18, 38)
                d(className="android.widget.EditText").send_keys(str(age))
                time.sleep(1)
                d.xpath('//*[@text="Tiếp"]').click()
                time.sleep(2)
                d.xpath('//*[@text="OK"]').click()
            tuoi_done_status = {"stt": stt_display, "trang_thai": "Đã nhập Tuổi = {age}", "ten_may": device_id, "ket_qua": "", "ho": random_ho, "ten": random_ten, "mat_khau": "", "email_sdt": "", "uid": "", "cookie": "", "token": "", "proxy": ""}
            self.status_manager.update_device_status(device_index, tuoi_done_status, self.table_manager)

            if d.xpath('//*[@text="Giới tính của bạn là gì?"]').wait(timeout=5):
                print("Giới tính của bạn là gì?")
                gender = random.choice(["Nam", "Nữ"])
                time.sleep(1)
                d.xpath(f'//*[@text="{gender}"]').click()
                time.sleep(1)
                d.xpath('//*[@text="Tiếp"]').click()
            sex_done_status = {"stt": stt_display, "trang_thai": "Chọn giới tính {gender} ", "ten_may": device_id, "ket_qua": "", "ho": random_ho, "ten": random_ten, "mat_khau": "", "email_sdt": "", "uid": "", "cookie": "", "token": "", "proxy": ""}
            self.status_manager.update_device_status(device_index, sex_done_status, self.table_manager)

            #### XỬ LÝ MỒI EMAIL/SĐT
            if d.xpath('//*[@text="Số di động của bạn là gì?" or @text="Email của bạn là gì?"]').wait(timeout=10):
                moi_type = self.moi_config.get('moi_type', 'khong_moi') if self.moi_config else 'khong_moi'
                logger.info(f"Detected moi type: {moi_type}")
                
                # Xác định loại mồi (Mail hay SĐT)
                is_mail_moi = moi_type in ['mail_theo_tep', 'duoi_mail']
                is_sdt_moi = moi_type in ['sdt_theo_tep', 'sdt_dau_so']
                
                if is_mail_moi:
                    # Trường hợp 1: User chọn mồi Mail
                    if d.xpath('//*[@text="Số di động của bạn là gì?"]').exists:
                        time.sleep(1)
                        d.xpath('//*[@text="Đăng ký bằng email"]').click()
                        time.sleep(2)
                    
                    # Lấy email data dựa trên loại mồi
                    if moi_type == 'mail_theo_tep':
                        mail_handler = MailTheoTepHandler()
                        email_data = mail_handler.mailtheotep()
                    else:  # duoi_mail
                        mail_handler = MailDuoiMailHandler()
                        email_data = mail_handler.duoimail()
                    
                    if email_data and d.xpath('//*[@text="Email của bạn là gì?"]').wait(timeout=5):
                        time.sleep(1)
                        d(className="android.widget.EditText").send_keys(email_data)
                        time.sleep(1)
                        d.xpath('//*[@text="Tiếp"]').click()
                        time.sleep(5)
                        if d.xpath('//*[@text="Bạn cần hỗ trợ đăng nhập vào tài khoản ư?"]').exists:
                            time.sleep(1)
                            d.xpath('//*[@text="Tiếp tục tạo tài khoản"]').click()
                            time.sleep(1)
                        email_status = {"stt": stt_display, "trang_thai": f"Đã nhập Email: {moi_type}", "ten_may": device_id, "ket_qua": "", "ho": random_ho, "ten": random_ten, "mat_khau": "", "email_sdt": email_data, "uid": "", "cookie": "", "token": "", "proxy": ""}
                        self.status_manager.update_device_status(device_index, email_status, self.table_manager)
                
                elif is_sdt_moi:
                    # Trường hợp 2: User chọn mồi SĐT
                    if d.xpath('//*[@text="Email của bạn là gì?"]').exists:
                        time.sleep(1)
                        d.xpath('//*[@text="Đăng ký bằng số di động"]').click()
                        time.sleep(2)
                    # Retry logic cho việc nhập SĐT (tối đa 3 lần thử)
                    sdt_success = False
                    sdt_data = None

                    for sdt_attempt in range(3):
                        logger.info(f"SĐT input attempt {sdt_attempt + 1}/3")

                        # Lấy SĐT data dựa trên loại mồi
                        if moi_type == 'sdt_theo_tep':
                            sdt_handler = SDTTheoTepHandler()
                            sdt_data = sdt_handler.sdttheotep()
                        else:  # sdt_dau_so
                            sdt_handler = SDTDauSoHandler()
                            sdt_data = sdt_handler.dauso()
                    
                        if sdt_data and d.xpath('//*[@text="Số di động của bạn là gì?"]').wait(timeout=5):
                            time.sleep(1)
                            # Clear field trước khi nhập (nếu có sẵn text)
                            input_field = d(className="android.widget.EditText")
                            if input_field.exists:
                                input_field.clear_text()
                                time.sleep(0.5)
                            # Nhập SĐT mới
                            input_field.send_keys(sdt_data)
                            time.sleep(1)
                            logger.info(f"👆 Clicking Tiếp button...")
                            d.xpath('//*[@text="Tiếp"]').click()
                            time.sleep(10)
                            if d.xpath('//*[@text="Tiếp tục tạo tài khoản"]').exists:
                                time.sleep(1)
                                d.xpath('//*[@text="Tiếp tục tạo tài khoản"]').click()
                                time.sleep(1)
                                break
                            if d.xpath('//*[@text="Tạo mật khẩu"]').exists:
                                break
                            # Kiểm tra lỗi "Số di động không hợp lệ"
                            if d.xpath('//*[@text="Số di động"]').exists:
                                logger.warning(f"❌ Error found with content-desc")
                                continue                        
                        else:
                            logger.error(f"Không lấy được SĐT hoặc không tìm thấy field nhập (lần {sdt_attempt + 1})")
                
                if sdt_success:    
                        sdt_status = {"stt": stt_display, "trang_thai": f"Đã nhập SĐT: {moi_type}", "ten_may": device_id, "ket_qua": "", "ho": random_ho, "ten": random_ten, "mat_khau": "", "email_sdt": sdt_data, "uid": "", "cookie": "", "token": "", "proxy": ""}
                        self.status_manager.update_device_status(device_index, sdt_status, self.table_manager)
                else:
                    # Không có mồi được chọn
                    no_moi_status = {"stt": stt_display, "trang_thai": "Không có mồi được chọn - dừng tại bước nhập Email/SĐT", "ten_may": device_id, "ket_qua": "", "ho": random_ho, "ten": random_ten, "mat_khau": "", "email_sdt": "", "uid": "", "cookie": "", "token": "", "proxy": ""}
                    self.status_manager.update_device_status(device_index, no_moi_status, self.table_manager)

            #### XỬ LÝ PASSWORD
            if d.xpath('//*[@text="Tạo mật khẩu"]').wait(timeout=10):
                password_config = get_password_configuration()
                password_type = password_config.get('password_type', 'randompass')
                custom_password = password_config.get('custom_password', '')
                
                password_result = xu_ly_buoc1.xu_ly_password(password_type, custom_password)
                
                if password_result.get('success'):
                    generated_password = password_result.get('password', '')
                    time.sleep(1)
                    d(className="android.widget.EditText").send_keys(generated_password)
                    time.sleep(1)
                    d.xpath('//*[@text="Tiếp"]').click()
                    time.sleep(3)
                    password_status = {"stt": stt_display, "trang_thai": f"Đã nhập Password: {password_result.get('type', 'unknown')}", "ten_may": device_id, "ket_qua": "", "ho": random_ho, "ten": random_ten, "mat_khau": generated_password, "email_sdt": sdt_data if 'sdt_data' in locals() else (email_data if 'email_data' in locals() else ""), "uid": "", "cookie": "", "token": "", "proxy": ""}
                    self.status_manager.update_device_status(device_index, password_status, self.table_manager)
                else:
                    error_password_status = {"stt": stt_display, "trang_thai": f"Lỗi tạo password: {password_result.get('message', 'Unknown error')}", "ten_may": device_id, "ket_qua": "Lỗi", "ho": random_ho, "ten": random_ten, "mat_khau": "", "email_sdt": sdt_data if 'sdt_data' in locals() else (email_data if 'email_data' in locals() else ""), "uid": "", "cookie": "", "token": "", "proxy": ""}
                    self.status_manager.update_device_status(device_index, error_password_status, self.table_manager)

            if d.xpath('//*[@text="Lúc khác"]').wait(timeout=5):
                time.sleep(1)
                d.xpath('//*[@text="Lúc khác"]').click()

            if d.xpath('//*[@text="Tôi đồng ý"]').wait(timeout=15):
                print("Tôi đồng ý xuất hiện")
            


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
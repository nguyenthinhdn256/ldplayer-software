import logging
import requests
import time
from typing import Dict, Any

logger = logging.getLogger(__name__)

class MailThueSimHandler:
    """Xử lý verification qua Gmail thuesim.app"""
    def __init__(self, api_key=None, gmail_account=None):
        self.api_key = api_key
        self.gmail_account = gmail_account
        logger.info(f"Khởi tạo MailThueSimHandler với API: {api_key}")
    
    def verify(self):
        """Logic xử lý verification cho thuesim.app"""
        logger.info("Đang xử lý verification qua thuesim.app")
        # TODO: Thêm logic xử lý ở đây
        pass

class MailIronSimHandler:
    """Xử lý verification qua Gmail ironsim.com"""
    def __init__(self, api_key=None):
        self.api_key = api_key
        logger.info(f"Khởi tạo MailIronSimHandler với API: {api_key}")
    
    def verify(self):
        """Logic xử lý verification cho ironsim.com"""
        logger.info("Đang xử lý verification qua ironsim.com")
        # TODO: Thêm logic xử lý ở đây
        pass

class RegClone2FAHandler:
    """Xử lý verification qua Hotmail regclone2fa.com"""
    def __init__(self, api_key=None):
        self.api_key = api_key
        logger.info(f"Khởi tạo RegClone2FAHandler với API: {api_key}")
    
    def verify(self):
        """Logic xử lý verification cho regclone2fa.com"""
        logger.info("Đang xử lý verification qua regclone2fa.com")
        # TODO: Thêm logic xử lý ở đây
        pass

class DongVanFBHandler:
    """Xử lý verification qua Hotmail dongvanfb.net"""
    def __init__(self, api_key=None, account=None):
        self.api_key = api_key
        self.account = account
        logger.info(f"Khởi tạo DongVanFBHandler với API: {api_key}")
    
    def verify(self):
        """Logic xử lý verification cho dongvanfb.net"""
        logger.info("Đang xử lý verification qua dongvanfb.net")
        # TODO: Thêm logic xử lý ở đây
        pass

class InputMailHandler:
    """Xử lý verification qua Input Mail"""
    def __init__(self):
        logger.info("Khởi tạo InputMailHandler")
    
    def verify(self):
        """Logic xử lý verification cho Input Mail"""
        logger.info("Đang xử lý verification qua Input Mail")
        # TODO: Thêm logic xử lý ở đây
        pass

class SimVIOTPHandler:
    """Xử lý verification qua SIM viotp.com"""
    def __init__(self, api_key=None):
        self.api_key = api_key
        logger.info(f"Khởi tạo SimVIOTPHandler với API: {api_key}")
    
    def verify(self):
        """Logic xử lý verification cho viotp.com"""
        logger.info("Đang xử lý verification qua viotp.com")
        # TODO: Thêm logic xử lý ở đây
        pass

class SMSIronSimHandler:
    """Xử lý verification qua SIM ironsim.com"""
    def __init__(self, api_key=None, account=None):
        self.api_key = api_key
        self.account = account

        logger.info(f"Khởi tạo SMSIronSimHandler với API: {api_key}")
    
    def verify(self, device, device_id: str, device_index: int):
        """Logic xử lý verification cho ironsim.com SMS"""
        logger.info("Đang xử lý verification qua ironsim.com SMS")
        
        if device.xpath('//*[@text="Nhập mã xác nhận"]').exists(timeout=5):
            time.sleep(1)
            device.xpath('//*[@text="Tôi không nhận được mã"]').click()

        pass

class FunOTPHandler:
    """Xử lý verification qua SIM funotp.com"""
    def __init__(self, api_key=None, parent_window=None):
        self.api_key = api_key
        self.parent_window = parent_window
        self.base_url = "https://funotp.com/api"
        logger.info(f"Khởi tạo FunOTPHandler với API: {api_key}")

    def rent_number(self):
        """Thuê số điện thoại từ FunOTP API - không chỉ định operator"""
        try:
            if not self.api_key and self.parent_window:
                self.api_key = get_sms_api_key('funotp', self.parent_window)

            if not self.api_key:
                logger.error("API key không được cung cấp")
                return {"success": False, "error": "API key không được cung cấp"}
            
            # Tham số request - không chỉ định operator
            params = { "action": "number", "service": "facebook", "apikey": self.api_key }

            logger.info(f"Đang request thuê số với params: {params}")
            
            # Gửi request
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            
            # Parse JSON response
            result = response.json()
            logger.info(f"API Response: {result}")
            
            # Kiểm tra response code
            if result.get("ResponseCode") == 0 and "Result" in result:
                number = result["Result"].get("number")
                sim_id = result["Result"].get("id")
                operator = result["Result"].get("operator", "Unknown")
                price = result["Result"].get("price")
                balance = result["Result"].get("balance")
                
                if number and sim_id:
                    logger.info(f"✅ Thuê số thành công: {number} (ID: {sim_id}) - Operator: {operator}")
                    return { "success": True, "number": number, "id": sim_id, "operator": operator, "price": price, "balance": balance, "full_response": result["Result"] }
                else:
                    logger.error(f"Response thiếu thông tin: {result}")
                    return {"success": False, "error": "Response thiếu number hoặc id"}
            else:
                error_msg = result.get("Message", "Unknown error")
                response_code = result.get("ResponseCode")
                logger.error(f"API error: ResponseCode={response_code}, Message={error_msg}")
                return {"success": False, "error": f"API error: {error_msg} (Code: {response_code})"}
                    
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error khi thuê số FunOTP: {e}")
            return {"success": False, "error": f"Network error: {str(e)}"}
        except ValueError as e:
            logger.error(f"JSON parse error: {e}")
            return {"success": False, "error": f"Invalid JSON response: {str(e)}"}
        except Exception as e:
            logger.error(f"Unexpected error khi thuê số FunOTP: {e}")
            return {"success": False, "error": f"Unexpected error: {str(e)}"}

    def get_otp_code(self, sim_id: str, max_attempts: int = 12, delay: int = 5):
        """Nhận mã OTP từ FunOTP API với retry - 12 lần, mỗi lần 5s"""
        import time
        
        try:
            # Lấy API key từ GUI nếu chưa có
            if not self.api_key and self.parent_window:
                self.api_key = get_sms_api_key('funotp', self.parent_window)
            
            if not self.api_key or not sim_id:
                return {"success": False, "error": "Thiếu API key hoặc Sim ID"}
            
            logger.info(f"🔄 Bắt đầu lấy OTP cho ID: {sim_id} - {max_attempts} lần, mỗi lần {delay}s")
            
            # Retry loop - 12 lần, mỗi lần 5s
            for attempt in range(max_attempts):
                logger.info(f"Lần thử lấy OTP {attempt + 1}/{max_attempts} cho ID: {sim_id}")
                
                try:
                    # Request API
                    url = f"{self.base_url}?action=code&id={sim_id}&apikey={self.api_key}"
                    response = requests.get(url, timeout=30)
                    result = response.json()
                    
                    logger.info(f"📋 API Response: {result}")
                    
                    # Kiểm tra response
                    if result.get("ResponseCode") == 0 and "Result" in result:
                        otp_code = result["Result"].get("otp")
                        sms_content = result["Result"].get("SMS")
                        
                        if otp_code:
                            logger.info(f"✅ Lấy OTP thành công: {otp_code}")
                            return { "success": True, "otp": otp_code, "sms": sms_content, "attempt": attempt + 1 }
                    
                    # ResponseCode != 0 hoặc chưa có OTP
                    logger.info(f"⏳ Chưa có OTP (ResponseCode: {result.get('ResponseCode')})")
                    
                    # Đợi và thử lại (trừ lần cuối)
                    if attempt < max_attempts - 1:
                        logger.info(f"⏳ Đợi {delay}s trước lần thử tiếp theo...")
                        time.sleep(delay)
                        
                except Exception as request_error:
                    logger.error(f"❌ Lỗi request lần {attempt + 1}: {request_error}")
                    if attempt < max_attempts - 1:
                        time.sleep(delay)
            
            # Hết số lần thử
            logger.error(f"❌ Không nhận được OTP sau {max_attempts} lần thử")
            return { "success": False, "error": f"Không nhận được OTP sau {max_attempts} lần thử ({max_attempts * delay}s)", "total_attempts": max_attempts }
            
        except Exception as e:
            logger.error(f"❌ Error getting OTP: {e}")
            return {"success": False, "error": str(e)}
    
    def execute_verification(self, device, device_id: str, device_index: int):
        """Function thực thi verification cho FunOTP"""
        try:
            logger.info(f"Bắt đầu thực thi verification FunOTP cho device {device_id}")
            
            # Kiểm tra và thực hiện các bước verification
            if device.xpath('//*[@text="Nhập mã xác nhận"]').exists:
                time.sleep(1)
                device.xpath('//*[@text="Tôi không nhận được mã"]').click()
                time.sleep(2)
                device.xpath('//*[@text="Đổi số di động"]').click()
                time.sleep(1)

                found_verification = False 
                for sdt_attempt in range(3):
                    if found_verification:  # Kiểm tra flag
                        break

                    # Thuê số điện thoại
                    rent_result = self.rent_number()
                    if not rent_result.get("success"):
                        return {"success": False, "error": f"Rent number failed: {rent_result.get('error')}"}
                    phone_number = rent_result.get("number")
                    sim_id = rent_result.get("id")
                    
                    input_field = device(className="android.widget.EditText")
                    if input_field.exists:
                        input_field.clear_text()
                        time.sleep(0.5)
                    # Nhập số điện thoại
                    input_field = device.xpath("//android.widget.EditText")
                    if input_field.exists:
                        input_field.set_text(phone_number)  # Thay send_keys bằng set_text
                    else:
                        return {"success": False, "error": "Không tìm thấy field nhập số điện thoại"}
                    time.sleep(1)
                    device.xpath('//*[@text="Tiếp"]').click()
                    xpaths = [
                        '//*[@text="Nhập mã xác nhận"]',
                        '//*[@text="Xác nhận số di động của bạn qua WhatsApp"]', 
                        '//*[@text="Xác nhận số di động qua SMS"]'
                    ]
                    for attempt in range(30):
                        if any(device.xpath(xpath).exists for xpath in xpaths):
                            print(f"Có ít nhất 1 button (lần thử {attempt + 1})")
                            found_verification = True
                            break
                        time.sleep(1)  # Đợi 1 giây trước lần thử tiếp theo
                    
                    if found_verification:  # Kiểm tra flag để thoát vòng lặp 3
                        break

                    if device.xpath('//*[@text="Số di động"]').exists:
                        logger.warning("Số  đã sử dụng. Tiếp tục thuê")
                        continue  
                    time.sleep(2)

                if device.xpath('//*[@text="Xác nhận số di động của bạn qua WhatsApp" or @text="Xác nhận số di động qua SMS"]').exists:
                    time.sleep(1)
                    if device.xpath('//*[@text="Thử cách khác"]').exists:
                        time.sleep(1)
                        device.xpath('//*[@text="Thử cách khác"]').click()
                        time.sleep(1)
                    if device.xpath('//*[@text="Gửi mã qua SMS"]').exists:
                        time.sleep(1)
                        device.xpath('//*[@text="Gửi mã qua SMS"]').click()
                        time.sleep(1)
                        device.xpath('//*[@text="Tiếp tục"]').click()

                time.sleep(5)
                
                # Nhận OTP code
                otp_result = self.get_otp_code(sim_id)
                if not otp_result.get("success"):
                    return {"success": False, "error": f"Get OTP failed: {otp_result.get('error')}"}
                otp_code = otp_result.get("otp")
                time.sleep(1)
                otp_field = device.xpath("//android.widget.EditText")
                if otp_field.exists:
                    otp_field.set_text(otp_code)  # Thay send_keys bằng set_text
                else:
                    return {"success": False, "error": "Không tìm thấy field nhập OTP"}
                time.sleep(1)
                # device.xpath('//*[@text="Tiếp"]').click()


                logger.info(f"Đã thực hiện các bước verification cho device {device_id}")
                return {"success": True, "message": "Verification steps completed"}
            else:
                logger.warning(f"Không tìm thấy màn hình 'Nhập mã xác nhận' trên device {device_id}")
                return {"success": False, "error": "Không tìm thấy màn hình xác nhận"}
                
        except Exception as e:
            logger.error(f"Lỗi khi thực thi verification FunOTP cho device {device_id}: {e}")
            return {"success": False, "error": str(e)}

class FiveSimHandler:
    """Xử lý verification qua SIM 5sim.com"""
    def __init__(self, api_key=None):
        self.api_key = api_key
        logger.info(f"Khởi tạo FiveSimHandler với API: {api_key}")
    
    def verify(self):
        """Logic xử lý verification cho 5sim.com"""
        logger.info("Đang xử lý verification qua 5sim.com")
        # TODO: Thêm logic xử lý ở đây
        pass

class SMS368Handler:
    """Xử lý verification qua SIM 368sms.com"""
    def __init__(self, api_key=None):
        self.api_key = api_key
        logger.info(f"Khởi tạo SMS368Handler với API: {api_key}")
    
    def verify(self):
        """Logic xử lý verification cho 368sms.com"""
        logger.info("Đang xử lý verification qua 368sms.com")
        # TODO: Thêm logic xử lý ở đây
        pass

class HCOTPHandler:
    """Xử lý verification qua SIM hcotp.com"""
    def __init__(self, api_key=None):
        self.api_key = api_key
        logger.info(f"Khởi tạo HCOTPHandler với API: {api_key}")
    
    def verify(self):
        """Logic xử lý verification cho hcotp.com"""
        logger.info("Đang xử lý verification qua hcotp.com")
        # TODO: Thêm logic xử lý ở đây
        pass

class SMSThueSimHandler:
    """Xử lý verification qua SIM thuesim.app"""
    def __init__(self, api_key=None, gmail_account=None):
        self.api_key = api_key
        self.gmail_account = gmail_account
        logger.info(f"Khởi tạo SMSThueSimHandler với API: {api_key}")
    
    def verify(self):
        """Logic xử lý verification cho thuesim.app SMS"""
        logger.info("Đang xử lý verification qua thuesim.app SMS")
        # TODO: Thêm logic xử lý ở đây
        pass

class Sim24Handler:
    """Xử lý verification qua SIM sim24.cc"""
    def __init__(self, api_key=None):
        self.api_key = api_key
        logger.info(f"Khởi tạo Sim24Handler với API: {api_key}")
    
    def verify(self):
        """Logic xử lý verification cho sim24.cc"""
        logger.info("Đang xử lý verification qua sim24.cc")
        # TODO: Thêm logic xử lý ở đây
        pass

class VerificationHandlerFactory:
    """Factory class để tạo handler phù hợp"""
    
    @staticmethod
    def create_handler(handler_type, **kwargs):
        handlers = {
            'mailthuesim': MailThueSimHandler,
            'mailironsim': MailIronSimHandler,
            'regclone2fa': RegClone2FAHandler,
            'dongvanfb': DongVanFBHandler,
            'inputmail': InputMailHandler,
            'simviotp': SimVIOTPHandler,
            'smsironsim': SMSIronSimHandler,
            'funotp': FunOTPHandler,
            '5sim': FiveSimHandler,
            '368sms': SMS368Handler,
            'hcotp': HCOTPHandler,
            'smsthuesim': SMSThueSimHandler,
            'sim24': Sim24Handler
        }
        
        handler_class = handlers.get(handler_type)
        if handler_class:
            return handler_class(**kwargs)
        else:
            logger.error(f"Không tìm thấy handler cho loại: {handler_type}")
            return None
        

# Config để lấy api key từ Gui        
def get_sms_api_key(sms_type: str, parent_window=None) -> str:
    # Mapping từ sms_type đến tên field trong GUI
    field_mapping = {
        'simviotp': 'sim_viotp_input',
        'smsironsim': 'sim_smsironsim_input2',  # Input thứ 2 chứa API key
        'funotp': 'sim_funotp_input',
        '5sim': 'sim_5sim_input',
        '368sms': 'sim_368sms_input',
        'hcotp': 'sim_hcotp_input',
        'smsthuesim': 'sim_smsthuesim_input',
        'sim24': 'sim_sim24_input'
    }
    
    try:
        # Kiểm tra sms_type hợp lệ
        if sms_type not in field_mapping:
            logger.error(f"SMS type không hợp lệ: {sms_type}")
            return ""
        field_name = field_mapping[sms_type]
        # Traverse để tìm app window
        app_window = parent_window
        while app_window and not hasattr(app_window, 'groupbox4_manager'):
            app_window = app_window.master if hasattr(app_window, 'master') else None
        
        if app_window and hasattr(app_window, 'groupbox4_manager'):
            groupbox4_manager = app_window.groupbox4_manager
            
            # Kiểm tra groupbox2_manager và field cụ thể
            if (hasattr(groupbox4_manager, 'groupbox2_manager') and 
                hasattr(groupbox4_manager.groupbox2_manager, field_name)):
                
                input_field = getattr(groupbox4_manager.groupbox2_manager, field_name)
                api_key = input_field.get().strip()
                return api_key if api_key else ""
        return ""
        
    except Exception as e:
        logger.error(f"Error getting {sms_type} API key: {e}")
        return ""
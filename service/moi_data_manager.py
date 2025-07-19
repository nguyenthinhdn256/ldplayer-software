import logging
import random
import os
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class KhongMoiHandler:
    """Handler cho trường hợp không mồi"""
    def __init__(self):
        self.provider_name = "Không Mồi"
    
    def generate_data(self, **kwargs) -> Dict[str, Any]:
        logger.info("Không sử dụng mồi - tạo data random")
        return {"status": "no_moi", "data": None, "message": "Không mồi"}

class MailTheoTepHandler:
    """Handler cho mồi Mail Theo Tệp"""
    def __init__(self):
        self.provider_name = "Mồi Mail Theo Tệp"
        self.file_path = "dulieu/mailphone/mailtheotep.txt"
    
    def generate_data(self, **kwargs) -> Dict[str, Any]:
        try:
            # Đọc file mail
            emails = self._read_data_file()
            if emails:
                selected_email = random.choice(emails)
                logger.info(f"Selected email: {selected_email}")
                return {"status": "success", "data": selected_email, "type": "email"}
            else:
                return {"status": "error", "message": "Không có email trong file"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def mailtheotep(self) -> str:
        """Đọc và lấy random 1 email duy nhất từ file mailtheotep.txt"""
        try:
            emails = self._read_data_file()
            if emails:
                selected_email = random.choice(emails)
                logger.info(f"Random email selected: {selected_email}")
                return selected_email
            else:
                logger.error("Không có email nào trong file mailtheotep.txt")
                return ""
        except Exception as e:
            logger.error(f"Lỗi khi đọc file mailtheotep.txt: {str(e)}")
            return ""
    
    def _read_data_file(self) -> List[str]:
        """Đọc dữ liệu từ file"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f.readlines() if line.strip() and not line.startswith('#')]
                return lines
        except FileNotFoundError:
            logger.error(f"File not found: {self.file_path}")
            return []

class SDTTheoTepHandler:
    """Handler cho mồi SĐT Theo Tệp"""
    def __init__(self):
        self.provider_name = "Mồi SĐT Theo Tệp"
        self.file_path = "dulieu/mailphone/sdttheotep.txt"
    
    def generate_data(self, **kwargs) -> Dict[str, Any]:
        try:
            sdts = self._read_data_file()
            if sdts:
                selected_sdt = random.choice(sdts)
                logger.info(f"Selected SDT: {selected_sdt}")
                return {"status": "success", "data": selected_sdt, "type": "sdt"}
            else:
                return {"status": "error", "message": "Không có SĐT trong file"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def sdttheotep(self) -> str:
        """Đọc và lấy random 1 SĐT duy nhất từ file sdttheotep.txt"""
        try:
            sdts = self._read_data_file()
            if sdts:
                selected_sdt = random.choice(sdts)
                logger.info(f"Random SDT selected: {selected_sdt}")
                return selected_sdt
            else:
                logger.error("Không có SĐT nào trong file sdttheotep.txt")
                return ""
        except Exception as e:
            logger.error(f"Lỗi khi đọc file sdttheotep.txt: {str(e)}")
            return ""
    
    def _read_data_file(self) -> List[str]:
        """Đọc dữ liệu từ file"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f.readlines() if line.strip() and not line.startswith('#')]
                return lines
        except FileNotFoundError:
            logger.error(f"File not found: {self.file_path}")
            return []

class MailDuoiMailHandler:
    """Handler cho mồi Theo Đầu Mail"""
    def __init__(self):
        self.provider_name = "Mồi Theo Đầu Mail"
        self.file_path = "dulieu/mailphone/daumail.txt"
    
    def generate_data(self, **kwargs) -> Dict[str, Any]:
        try:
            # Đọc danh sách đầu mail
            dau_mails = self._read_data_file()
            if dau_mails:
                selected_dau = random.choice(dau_mails)
                # Tạo email random với đầu này
                random_number = random.randint(1000, 9999)
                generated_email = f"{selected_dau}{random_number}@gmail.com"
                return {"status": "success", "data": generated_email, "type": "generated_email"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

class SDTDauSoHandler:
    """Handler cho mồi Theo Đầu Số"""
    def __init__(self):
        self.provider_name = "Mồi Theo Đầu Số"
        self.file_path = "dulieu/mailphone/dauso.txt"
    
    def generate_data(self, **kwargs) -> Dict[str, Any]:
        try:
            # Đọc danh sách đầu số
            dau_sos = self._read_data_file()
            if dau_sos:
                selected_dau = random.choice(dau_sos)
                # Tạo SĐT random với đầu này  
                random_digits = ''.join([str(random.randint(0, 9)) for _ in range(7)])
                generated_sdt = f"{selected_dau}{random_digits}"
                return {"status": "success", "data": generated_sdt, "type": "generated_sdt"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

class MoiDataFactory:
    """Factory class để tạo handler phù hợp"""
    
    @staticmethod
    def create_handler(handler_type, **kwargs):
        handlers = {
            'khong_moi': KhongMoiHandler,
            'mail_theo_tep': MailTheoTepHandler,
            'sdt_theo_tep': SDTTheoTepHandler,
            'sdt_dau_mail': MailDuoiMailHandler,
            'sdt_dau_so': SDTDauSoHandler
        }
        
        handler_class = handlers.get(handler_type)
        if handler_class:
            return handler_class(**kwargs)
        else:
            logger.error(f"Không tìm thấy handler cho loại: {handler_type}")
            return None
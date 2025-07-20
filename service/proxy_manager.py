# -*- coding: utf-8 -*-
"""
Ver Proxy Service - Xử lý verification proxy với 5 loại provider
"""
import logging, time, subprocess
from typing import Dict, Any

logger = logging.getLogger(__name__)

class NoProxyHandler:
    """Handler cho trường hợp không dùng proxy"""
    def __init__(self, config_data: str = ""):
        self.config_data = config_data
        self.provider_name = "Không Dùng Proxy"
    
    def process_proxy(self, **kwargs) -> Dict[str, Any]:
        logger.info(f"Processing with {self.provider_name}")
        return {"status": "ready", "provider": self.provider_name, "format": "no_proxy", "data": ""}
    
    def setup_no_proxy(self, **kwargs) -> Dict[str, Any]:
        """Thiết lập chế độ không dùng proxy cho script chính"""
        logger.info("Setting up no proxy mode for script execution")
        return {"success": True, "mode": "no_proxy", "provider": self.provider_name, "message": "No proxy will be used"}

class HostPortUserPassHandler:
    """Handler cho Host:Port:User:Pass proxy format"""
    def __init__(self, config_data: str = ""):
        self.config_data = config_data
        self.provider_name = "Host:Port:User:Pass"
    
    def process_proxy(self, **kwargs) -> Dict[str, Any]:
        logger.info(f"Processing proxy with {self.provider_name}")
        return {"status": "ready", "provider": self.provider_name, "format": "host:port:user:pass", "data": self.config_data}

class HostPortNenDungHandler:
    """Handler cho Host:Port (Nên Dùng) proxy format"""
    def __init__(self, config_data: str = ""):
        self.config_data = config_data
        self.provider_name = "Host:Port (Nên Dùng)"
    
    def process_proxy(self, **kwargs) -> Dict[str, Any]:
        logger.info(f"Processing proxy with {self.provider_name}")
        return {"status": "ready", "provider": self.provider_name, "format": "host:port", "data": self.config_data}

class Vn2rayHandler:
    """Handler cho Vn2ray proxy provider"""
    def __init__(self, config_data: str = ""):
        self.config_data = config_data
        self.provider_name = "Vn2ray"
    
    def process_proxy(self, **kwargs) -> Dict[str, Any]:
        logger.info(f"Processing proxy with {self.provider_name}")
        return {"status": "ready", "provider": self.provider_name, "format": "vn2ray", "data": self.config_data}

class WWProxyHandler:
    """Handler cho WW Proxy provider"""
    def __init__(self, config_data: str = ""):
        self.config_data = config_data
        self.provider_name = "WW Proxy"
    
    def process_proxy(self, **kwargs) -> Dict[str, Any]:
        logger.info(f"Processing proxy with {self.provider_name}")
        return {"status": "ready", "provider": self.provider_name, "format": "wwproxy", "data": self.config_data}
    
    def setup_proxy(self, device, device_index=0, **kwargs) -> Dict[str, Any]:
        """Thiết lập WW Proxy - khởi chạy app và đọc proxy data"""
        try:
            logger.info("Bắt đầu setup WW Proxy")
            
            # ĐỌC PROXY DATA
            proxy_file = f"Profile/Profile-{device_index + 1}/wwproxy.txt"
            with open(proxy_file, 'r', encoding='utf-8') as f:
                proxies = [line.strip() for line in f.readlines() if line.strip()]
            
            proxy_data = proxies[device_index % len(proxies)] if proxies else ""
            logger.info(f"Using proxy: {proxy_data}")
            device.set_clipboard(proxy_data)
            
            # Khởi chạy app WW Proxy
            device.app_start('com.hct.myapplication')

            time.sleep(5)
            device.xpath('//*[@resource-id="com.hct.myapplication:id/btnPaste"]').click()
            time.sleep(1)
            if device(text="TẮT").exists:
                device(text="TẮT").click()
            time.sleep(2)
            if device(text="OK").exists:
                device(text="OK").click()
            time.sleep(5)
            device.app_stop('com.hct.myapplication')

            return { "success": True, "provider": "WW Proxy", "proxy_data": proxy_data, "message": "WW Proxy setup completed" }
            
        except Exception as e:
            logger.error(f"Error setting up WW Proxy: {str(e)}")
            return {"success": False, "error": str(e)}

    def change_ip(self, device, device_index=0, **kwargs) -> Dict[str, Any]:
        try:
            logger.info("Bắt đầu thây đổi ip WW Proxy")

            # Khởi chạy app WW Proxy
            device.app_start('com.hct.myapplication')
            time.sleep(5)
            device.xpath('//*[@resource-id="com.hct.myapplication:id/btnChangeIP"]').click()
            time.sleep(5)
            device.app_stop('com.hct.myapplication')

        except Exception as e:
            logger.error(f"Error setting up WW Proxy: {str(e)}")
            return {"success": False, "error": str(e)}
            
            
class ProxyNo1Handler:
    """Handler cho Proxy No1 provider"""
    def __init__(self, config_data: str = ""):
        self.config_data = config_data
        self.provider_name = "Proxy No1"
    
    def process_proxy(self, **kwargs) -> Dict[str, Any]:
        logger.info(f"Processing proxy with {self.provider_name}")
        return {"status": "ready", "provider": self.provider_name, "format": "proxyno1", "data": self.config_data}

class VerProxyService:
    """Service quản lý verification proxy với mapping provider"""
    PROVIDER_MAPPING = {"host_port_user_pass": HostPortUserPassHandler, "host_port_nen_dung": HostPortNenDungHandler, "vn2ray": Vn2rayHandler, "ww_proxy": WWProxyHandler, "proxy_no1": ProxyNo1Handler}
    
    def __init__(self):
        self.current_provider = None
        self.current_handler = None
        self.config_data = ""
    
    def set_provider(self, provider_key: str, config_data: str = "") -> bool:
        """Thiết lập provider và tạo handler tương ứng"""
        if provider_key not in self.PROVIDER_MAPPING:
            logger.error(f"Unknown proxy provider: {provider_key}")
            return False
        handler_class = self.PROVIDER_MAPPING[provider_key]
        self.current_handler = handler_class(config_data)
        self.current_provider = provider_key
        self.config_data = config_data
        logger.info(f"Set proxy provider: {self.current_handler.provider_name}")
        return True
    
    def process_proxy_verification(self, **kwargs) -> Dict[str, Any]:
        """Xử lý verification proxy với provider hiện tại"""
        if not self.current_handler:
            return {"success": False, "error": "no_provider", "message": "No proxy provider selected"}
        return self.current_handler.process_proxy(**kwargs)
    
    def get_current_provider_info(self) -> Dict[str, str]:
        """Lấy thông tin provider hiện tại"""
        if not self.current_handler:
            return {"provider": "none", "name": "No proxy provider selected", "config_data": ""}
        return {"provider": self.current_provider, "name": self.current_handler.provider_name, "config_data": self.config_data}
    
    def is_ready(self) -> bool:
        """Kiểm tra service đã sẵn sàng xử lý"""
        return self.current_handler is not None and bool(self.config_data.strip())
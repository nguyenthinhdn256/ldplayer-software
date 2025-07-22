import logging, time, subprocess
from typing import Dict, Any

logger = logging.getLogger(__name__)

class NoProxyHandler:
    def __init__(self, config_data: str = ""):
        self.config_data = config_data
        self.provider_name = "Không Dùng Proxy"
    
    def process_proxy(self, **kwargs) -> Dict[str, Any]:
        logger.info(f"Processing with {self.provider_name}")
        return {"status": "ready", "provider": self.provider_name, "format": "no_proxy", "data": ""}
    
    def setup_no_proxy(self, device, device_index=0, **kwargs) -> Dict[str, Any]:
        logger.info("Setting up no proxy mode for script execution")
        return {"success": True, "mode": "no_proxy", "provider": self.provider_name, "message": "No proxy will be used"}

class HostPortUserPassHandler:
    def __init__(self, config_data: str = ""):
        self.config_data = config_data
        self.provider_name = "Host:Port:User:Pass"
    
    def process_proxy(self, **kwargs) -> Dict[str, Any]:
        logger.info(f"Processing proxy with {self.provider_name}")
        return {"status": "ready", "provider": self.provider_name, "format": "host:port:user:pass", "data": self.config_data}
    
    def setup_proxy(self, device, device_index=0, **kwargs) -> Dict[str, Any]:
        try:
            logger.info("Setting up Host:Port:User:Pass proxy")
            proxy_file = f"Profile/Profile-{device_index + 1}/hostport.txt"
            with open(proxy_file, 'r', encoding='utf-8') as f:
                proxies = [line.strip() for line in f.readlines() if line.strip()]
            proxy_data = proxies[device_index % len(proxies)] if proxies else ""
            logger.info(f"Using proxy: {proxy_data}")
            return {"success": True, "provider": "Host:Port:User:Pass", "proxy_data": proxy_data, "message": "Host:Port:User:Pass setup completed"}
        except Exception as e:
            logger.error(f"Error setting up Host:Port:User:Pass: {str(e)}")
            return {"success": False, "error": str(e)}

class HostPortNenDungHandler:
    def __init__(self, config_data: str = ""):
        self.config_data = config_data
        self.provider_name = "Host:Port (Nên Dùng)"
    
    def process_proxy(self, **kwargs) -> Dict[str, Any]:
        logger.info(f"Processing proxy with {self.provider_name}")
        return {"status": "ready", "provider": self.provider_name, "format": "host:port", "data": self.config_data}
    
    def setup_proxy(self, device, device_index=0, **kwargs) -> Dict[str, Any]:
        try:
            logger.info("Setting up Host:Port proxy")
            proxy_file = f"Profile/Profile-{device_index + 1}/hostport.txt"
            with open(proxy_file, 'r', encoding='utf-8') as f:
                proxies = [line.strip() for line in f.readlines() if line.strip()]
            proxy_data = proxies[device_index % len(proxies)] if proxies else ""
            logger.info(f"Using proxy: {proxy_data}")
            return {"success": True, "provider": "Host:Port", "proxy_data": proxy_data, "message": "Host:Port setup completed"}
        except Exception as e:
            logger.error(f"Error setting up Host:Port: {str(e)}")
            return {"success": False, "error": str(e)}

class Vn2rayHandler:
    def __init__(self, config_data: str = ""):
        self.config_data = config_data
        self.provider_name = "Vn2ray"
    
    def process_proxy(self, **kwargs) -> Dict[str, Any]:
        logger.info(f"Processing proxy with {self.provider_name}")
        return {"status": "ready", "provider": self.provider_name, "format": "vn2ray", "data": self.config_data}
    
    def nhapip(self, device, device_index=0, **kwargs) -> Dict[str, Any]:
        try:
            logger.info("Setting up Vn2ray proxy")
            proxy_file = f"Profile/Profile-{device_index + 1}/vn2ray.txt"
            with open(proxy_file, 'r', encoding='utf-8') as f:
                proxies = [line.strip() for line in f.readlines() if line.strip()]
            proxy_data = proxies[device_index % len(proxies)] if proxies else ""
            logger.info(f"Using proxy: {proxy_data}")
            device.set_clipboard(proxy_data)
            device.app_start('com.v2ray.ang')
            time.sleep(5)
            device.xpath('//*[@resource-id="com.v2ray.ang:id/fab"]').click()
            time.sleep(2)
            device.xpath('//*[@text="Import config from clipboard"]').click()
            time.sleep(3)
            device.xpath('//*[@resource-id="com.v2ray.ang:id/fab"]').click()
            time.sleep(2)
            device.app_stop('com.v2ray.ang')
            return {"success": True, "provider": "Vn2ray", "proxy_data": proxy_data, "message": "Vn2ray setup completed"}
        except Exception as e:
            logger.error(f"Error setting up Vn2ray: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def change_ip(self, device, device_index=0, **kwargs) -> Dict[str, Any]:
        try:
            logger.info("Changing IP for Vn2ray")
            device.app_start('com.v2ray.ang')
            time.sleep(3)
            device.xpath('//*[@resource-id="com.v2ray.ang:id/fab"]').click()
            time.sleep(2)
            device.app_stop('com.v2ray.ang')
            return {"success": True, "message": "Vn2ray IP changed"}
        except Exception as e:
            logger.error(f"Error changing Vn2ray IP: {str(e)}")
            return {"success": False, "error": str(e)}

class WWProxyHandler:
    def __init__(self, config_data: str = ""):
        self.config_data = config_data
        self.provider_name = "WW Proxy"
    
    def process_proxy(self, **kwargs) -> Dict[str, Any]:
        logger.info(f"Processing proxy with {self.provider_name}")
        return {"status": "ready", "provider": self.provider_name, "format": "wwproxy", "data": self.config_data}
    
    def setup_proxy(self, device, device_index=0, **kwargs) -> Dict[str, Any]:
        try:
            logger.info("Setting up WW Proxy")
            proxy_file = f"Profile/Profile-{device_index + 1}/wwproxy.txt"
            with open(proxy_file, 'r', encoding='utf-8') as f:
                proxies = [line.strip() for line in f.readlines() if line.strip()]
            proxy_data = proxies[device_index % len(proxies)] if proxies else ""
            logger.info(f"Using proxy: {proxy_data}")
            device.set_clipboard(proxy_data)
            device.app_start('com.hct.myapplication')
            time.sleep(5)
            device.xpath('//*[@resource-id="com.hct.myapplication:id/btnPaste"]').click()
            time.sleep(1)
            device.xpath('//*[@resource-id="com.hct.myapplication:id/menu_item_switch"]').click()
            # if device(text="TẮT").exists:
            #     device(text="TẮT").click()
            if device(text="OK").wait(timeout=10):
                time.sleep(1)
                device(text="OK").click()
            time.sleep(10)

            device.app_stop('com.hct.myapplication')
            time.sleep(5)
            return {"success": True, "provider": "WW Proxy", "proxy_data": proxy_data, "message": "WW Proxy setup completed"}
        except Exception as e:
            logger.error(f"Error setting up WW Proxy: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def change_ip(self, device, device_index=0, **kwargs) -> Dict[str, Any]:
        try:
            logger.info("Changing IP for WW Proxy")
            time.sleep(5)
            device.app_start('com.hct.myapplication')
            time.sleep(5)
            device.xpath('//*[@resource-id="com.hct.myapplication:id/btnChangeIP"]').click()
            time.sleep(10)
            device.app_stop('com.hct.myapplication')
            time.sleep(5)
            return {"success": True, "message": "WW Proxy IP changed"}
        except Exception as e:
            logger.error(f"Error changing WW Proxy IP: {str(e)}")
            return {"success": False, "error": str(e)}

class ProxyNo1Handler:
    def __init__(self, config_data: str = ""):
        self.config_data = config_data
        self.provider_name = "Proxy No1"
    
    def process_proxy(self, **kwargs) -> Dict[str, Any]:
        logger.info(f"Processing proxy with {self.provider_name}")
        return {"status": "ready", "provider": self.provider_name, "format": "proxyno1", "data": self.config_data}
    
    def setup_proxy(self, device, device_index=0, **kwargs) -> Dict[str, Any]:
        try:
            logger.info("Setting up Proxy No1")
            proxy_file = f"Profile/Profile-{device_index + 1}/proxyno1.txt"
            with open(proxy_file, 'r', encoding='utf-8') as f:
                proxies = [line.strip() for line in f.readlines() if line.strip()]
            proxy_data = proxies[device_index % len(proxies)] if proxies else ""
            logger.info(f"Using proxy: {proxy_data}")
            device.set_clipboard(proxy_data)
            device.app_start('com.saturn.no1vpn1')
            time.sleep(5)
            device.xpath('//*[@resource-id="com.saturn.no1vpn1:id/btnConnect"]').click()
            time.sleep(3)
            device.app_stop('com.saturn.no1vpn1')
            return {"success": True, "provider": "Proxy No1", "proxy_data": proxy_data, "message": "Proxy No1 setup completed"}
        except Exception as e:
            logger.error(f"Error setting up Proxy No1: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def change_ip(self, device, device_index=0, **kwargs) -> Dict[str, Any]:
        try:
            logger.info("Changing IP for Proxy No1")
            device.app_start('com.saturn.no1vpn1')
            time.sleep(3)
            device.xpath('//*[@resource-id="com.saturn.no1vpn1:id/btnDisconnect"]').click()
            time.sleep(2)
            device.xpath('//*[@resource-id="com.saturn.no1vpn1:id/btnConnect"]').click()
            time.sleep(3)
            device.app_stop('com.saturn.no1vpn1')
            return {"success": True, "message": "Proxy No1 IP changed"}
        except Exception as e:
            logger.error(f"Error changing Proxy No1 IP: {str(e)}")
            return {"success": False, "error": str(e)}

class SuperProxyHandler:
    def __init__(self, config_data: str = ""):
        self.config_data = config_data
        self.provider_name = "Super Proxy"
    
    def process_proxy(self, **kwargs) -> Dict[str, Any]:
        logger.info(f"Processing proxy with {self.provider_name}")
        return {"status": "ready", "provider": self.provider_name, "format": "superproxy", "data": self.config_data}
    
    def setup_proxy(self, device, device_index=0, **kwargs) -> Dict[str, Any]:
        try:
            logger.info("Setting up Super Proxy")
            proxy_file = f"Profile/Profile-{device_index + 1}/superproxy.txt"
            with open(proxy_file, 'r', encoding='utf-8') as f:
                proxies = [line.strip() for line in f.readlines() if line.strip()]
            proxy_data = proxies[device_index % len(proxies)] if proxies else ""
            logger.info(f"Using proxy: {proxy_data}")
            device.app_start('com.scheler.superproxy')
            time.sleep(5)
            device.xpath('//*[@resource-id="com.scheler.superproxy:id/btnStart"]').click()
            time.sleep(3)
            device.app_stop('com.scheler.superproxy')
            return {"success": True, "provider": "Super Proxy", "proxy_data": proxy_data, "message": "Super Proxy setup completed"}
        except Exception as e:
            logger.error(f"Error setting up Super Proxy: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def change_ip(self, device, device_index=0, **kwargs) -> Dict[str, Any]:
        try:
            logger.info("Changing IP for Super Proxy")
            device.app_start('com.scheler.superproxy')
            time.sleep(3)
            device.xpath('//*[@resource-id="com.scheler.superproxy:id/btnRefresh"]').click()
            time.sleep(3)
            device.app_stop('com.scheler.superproxy')
            return {"success": True, "message": "Super Proxy IP changed"}
        except Exception as e:
            logger.error(f"Error changing Super Proxy IP: {str(e)}")
            return {"success": False, "error": str(e)}
            
            
class WindscribeVPNHandler:
    def __init__(self, config_data: str = ""):
        self.config_data = config_data
        self.provider_name = "Windscribe VPN"
    
    def process_proxy(self, **kwargs) -> Dict[str, Any]:
        logger.info(f"Processing proxy with {self.provider_name}")
        return {"status": "ready", "provider": self.provider_name, "format": "windscribe", "data": self.config_data}
    
    def setup_proxy(self, device, device_index=0, **kwargs) -> Dict[str, Any]:
        try:
            logger.info("Setting up Windscribe VPN")
            device.app_start('com.windscribe.vpn')
            time.sleep(5)
            device.xpath('//*[@resource-id="com.windscribe.vpn:id/btnConnect"]').click()
            time.sleep(5)
            device.app_stop('com.windscribe.vpn')
            return {"success": True, "provider": "Windscribe VPN", "message": "Windscribe VPN setup completed"}
        except Exception as e:
            logger.error(f"Error setting up Windscribe VPN: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def change_ip(self, device, device_index=0, **kwargs) -> Dict[str, Any]:
        try:
            logger.info("Changing IP for Windscribe VPN")
            device.app_start('com.windscribe.vpn')
            time.sleep(3)
            device.xpath('//*[@resource-id="com.windscribe.vpn:id/btnDisconnect"]').click()
            time.sleep(2)
            device.xpath('//*[@resource-id="com.windscribe.vpn:id/btnConnect"]').click()
            time.sleep(3)
            device.app_stop('com.windscribe.vpn')
            return {"success": True, "message": "Windscribe VPN IP changed"}
        except Exception as e:
            logger.error(f"Error changing Windscribe VPN IP: {str(e)}")
            return {"success": False, "error": str(e)}

class ProxyConfigManager:
    """Manager để xử lý cấu hình proxy giữa GUI và script logic"""
    
    PROXY_HANDLER_MAPPING = {"khong_dung_proxy": {"handler": NoProxyHandler, "function": "setup_no_proxy"}, "host_port_user_pass": {"handler": HostPortUserPassHandler, "function": "setup_proxy"}, "host_port": {"handler": HostPortNenDungHandler, "function": "setup_proxy"}, "vn2ray": {"handler": Vn2rayHandler, "function": "nhapip"}, "ww_proxy": {"handler": WWProxyHandler, "function": "setup_proxy"}, "proxy_no1": {"handler": ProxyNo1Handler, "function": "setup_proxy"}, "super_proxy": {"handler": SuperProxyHandler, "function": "setup_proxy"}, "windscribe_vpn": {"handler": WindscribeVPNHandler, "function": "setup_proxy"}}
    
    @staticmethod
    def get_proxy_config_from_gui(parent_window=None) -> Dict[str, Any]:
        """Lấy cấu hình proxy từ GUI"""
        try:
            app_window = parent_window
            while app_window and not hasattr(app_window, 'groupbox4_manager'):
                app_window = app_window.master if hasattr(app_window, 'master') else None
            
            if app_window and hasattr(app_window, 'groupbox4_manager'):
                groupbox4_manager = app_window.groupbox4_manager
                if hasattr(groupbox4_manager, 'groupbox5_manager'):
                    return groupbox4_manager.groupbox5_manager.get_proxy_configuration()
            
            return {"use_proxy": False, "proxy_type": "", "enabled": False}
        except Exception as e:
            logger.error(f"Error getting proxy configuration from GUI: {e}")
            return {"use_proxy": False, "proxy_type": "", "enabled": False}
    
    @staticmethod
    def execute_proxy_function(device, device_index: int, proxy_type: str, function_name: str) -> Dict[str, Any]:
        """Thực thi function cụ thể của proxy handler"""
        try:
            if proxy_type in ProxyConfigManager.PROXY_HANDLER_MAPPING:
                handler_class = ProxyConfigManager.PROXY_HANDLER_MAPPING[proxy_type]["handler"]
                handler_instance = handler_class()
                
                if function_name and hasattr(handler_instance, function_name):
                    proxy_function = getattr(handler_instance, function_name)
                    result = proxy_function(device, device_index)
                    logger.info(f"Executed {proxy_type}.{function_name}: {result}")
                    return result
                else:
                    logger.warning(f"Function {function_name} not found in {proxy_type}")
                    return {"success": False, "error": f"Function {function_name} not found"}
            else:
                logger.error(f"Unknown proxy type: {proxy_type}")
                return {"success": False, "error": f"Unknown proxy type: {proxy_type}"}
                
        except Exception as e:
            logger.error(f"Error executing {proxy_type}.{function_name}: {e}")
            return {"success": False, "error": str(e)}
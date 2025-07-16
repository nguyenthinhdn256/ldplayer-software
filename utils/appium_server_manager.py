import os, sys, subprocess, threading, time, logging, socket, requests
from typing import Optional, Dict, Any
from appium.webdriver.appium_service import AppiumService

logger = logging.getLogger(__name__)

class AppiumServerManager:
    """Clean and simple Appium Server Manager for TClone Register project"""

    def __init__(self, host: str = "127.0.0.1", port: int = 4723, timeout: int = 30, log_level: str = "info"):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.log_level = log_level
        self.service: Optional[AppiumService] = None
        self.is_running = False
        self.server_url = f"http://{host}:{port}"

    def is_port_available(self) -> bool:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)
                return sock.connect_ex((self.host, self.port)) != 0
        except Exception:
            return False

    def is_appium_server_running(self) -> bool:
        try:
            response = requests.get(f"{self.server_url}/status", timeout=5)
            return response.status_code == 200
        except Exception:
            return False

    def start_server(self) -> Dict[str, Any]:
        try:
            if self.is_appium_server_running():
                self.is_running = True
                return {"success": True, "message": f"Appium server already running on {self.server_url}", "server_url": self.server_url}
            
            if not self.is_port_available():
                return {"success": False, "message": f"Port {self.port} is already in use by another service", "server_url": None}
            
            try:
                import subprocess
                subprocess.run(["taskkill", "/F", "/IM", "node.exe"], capture_output=True, text=True)
                subprocess.run(["taskkill", "/F", "/IM", "appium.exe"], capture_output=True, text=True)
            except Exception:
                pass
            
            self.service = AppiumService()
            args = ['--address', self.host, '--port', str(self.port), '--base-path', '/', '--log-level', self.log_level, '--session-override', '--no-reset', '--local-timezone', '--allow-insecure', 'chromedriver_autodownload']
            self.service.start(args=args, timeout_ms=10000)
            
            start_time = time.time()
            while time.time() - start_time < self.timeout:
                if self.test_server_endpoints():
                    self.is_running = True
                    return {"success": True, "message": f"Appium server started successfully on {self.server_url}", "server_url": self.server_url}
                time.sleep(1.0)
            
            self.stop_server()
            return {"success": False, "message": f"Appium server failed to start within {self.timeout} seconds", "server_url": None}
            
        except Exception as e:
            logger.error(f"Error starting Appium server: {str(e)}")
            return {"success": False, "message": f"Failed to start Appium server: {str(e)}", "server_url": None}
        
    def test_server_endpoints(self) -> bool:
        """Test multiple endpoints để kiểm tra server có sẵn sàng không"""
        endpoints = ['/status', '/wd/hub/status', '/sessions']
        
        for endpoint in endpoints:
            try:
                url = f"{self.server_url}{endpoint}"
                response = requests.get(url, timeout=3)
                if response.status_code == 200:
                    return True
            except Exception:
                continue
        
        return False

    def stop_server(self) -> Dict[str, Any]:
        try:
            if self.service and self.service.is_running:
                self.service.stop()
                self.service = None
            self.is_running = False
            return {"success": True, "message": "Appium server stopped successfully"}
        except Exception as e:
            logger.error(f"Error stopping Appium server: {str(e)}")
            return {"success": False, "message": f"Failed to stop Appium server: {str(e)}"}

    def restart_server(self) -> Dict[str, Any]:
        stop_result = self.stop_server()
        if stop_result["success"]:
            time.sleep(2)
            return self.start_server()
        return stop_result

    def get_server_status(self) -> Dict[str, Any]:
        try:
            if self.is_appium_server_running():
                response = requests.get(f"{self.server_url}/status", timeout=5)
                return {"success": True, "running": True, "server_url": self.server_url, "details": response.json().get("value", {})}
            else:
                return {"success": True, "running": False, "server_url": self.server_url, "details": {}}
        except Exception as e:
            return {"success": False, "running": False, "server_url": self.server_url, "error": str(e)}

    def __enter__(self):
        result = self.start_server()
        if not result["success"]: raise Exception(result["message"])
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop_server()

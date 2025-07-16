import os
import sys
import subprocess
import threading
import time
import logging
import socket
import requests
from typing import Optional, Dict, Any, List
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger(__name__)

class AppiumServerManager:
    """Enhanced Appium Server Manager with subprocess execution"""

    def __init__(self, base_port: int = 4723, max_servers: int = 50, timeout: int = 45, log_level: str = "info"):
        self.base_port = base_port
        self.max_servers = max_servers
        self.timeout = timeout
        self.log_level = log_level
        self.servers = {}  # {port: subprocess.Popen}
        self.is_running = False
        
        # Port mapping: ADB port -> Appium port
        self.port_mapping = self._create_port_mapping()
        
    def _create_port_mapping(self) -> Dict[int, int]:
        """Tạo mapping giữa ADB ports (5554-5652) và Appium ports (4723-4772)"""
        mapping = {}
        adb_start = 5554
        appium_start = self.base_port
        
        for i in range(self.max_servers):
            adb_port = adb_start + (i * 2)  # ADB ports: 5554, 5556, 5558...
            appium_port = appium_start + i   # Appium ports: 4723, 4724, 4725...
            mapping[adb_port] = appium_port
            
        logger.info(f"Created port mapping for {len(mapping)} devices")
        return mapping
    
    def get_appium_port_for_device(self, device_id: str) -> Optional[int]:
        """Lấy Appium port tương ứng với device ID"""
        try:
            if device_id.startswith('emulator-'):
                adb_port = int(device_id.split('-')[1])
                return self.port_mapping.get(adb_port)
            return None
        except Exception as e:
            logger.error(f"Error getting port for device {device_id}: {e}")
            return None
    
    def is_port_available(self, port: int) -> bool:
        """Kiểm tra port có available không"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)
                return sock.connect_ex(("127.0.0.1", port)) != 0
        except Exception:
            return False

    def is_appium_server_running(self, port: int) -> bool:
        """Kiểm tra Appium server có đang chạy trên port không"""
        try:
            response = requests.get(f"http://127.0.0.1:{port}/status", timeout=8)
            return response.status_code == 200
        except Exception:
            return False

    def start_server_for_device(self, device_id: str) -> Dict[str, Any]:
        """Khởi động Appium server cho device cụ thể - FIXED ARGUMENTS"""
        try:
            appium_port = self.get_appium_port_for_device(device_id)
            if not appium_port:
                return {"success": False, "message": f"No port mapping for device {device_id}"}
            
            logger.info(f"Starting Appium server for {device_id} on port {appium_port}")
            
            # Kiểm tra server đã chạy chưa
            if appium_port in self.servers:
                process = self.servers[appium_port]
                if process.poll() is None and self.is_appium_server_running(appium_port):
                    return {
                        "success": True, 
                        "message": f"Appium server already running for {device_id}", 
                        "port": appium_port,
                        "server_url": f"http://127.0.0.1:{appium_port}"
                    }
                else:
                    # Process dead, remove from tracking
                    del self.servers[appium_port]
            
            # Kill process on port if needed
            if not self.is_port_available(appium_port):
                self._kill_process_on_port(appium_port)
                time.sleep(3)
            
            # Build command - FIXED ARGUMENTS
            cmd = [
                'appium',
                '--address', '127.0.0.1',
                '--port', str(appium_port),
                '--base-path', '/',
                '--log-level', self.log_level,
                '--session-override',
                '--local-timezone',
                '--allow-insecure', 'chromedriver_autodownload',
                '--relaxed-security'
            ]
            
            logger.info(f"Executing command: {' '.join(cmd)}")
            
            # Start process with subprocess
            try:
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    shell=True,
                    creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
                )
                
                logger.info(f"Process started with PID: {process.pid}")
                
            except FileNotFoundError:
                return {"success": False, "message": "Appium command not found. Please ensure Appium is installed and in PATH."}
            except Exception as e:
                return {"success": False, "message": f"Failed to start process: {str(e)}"}
            
            # Wait for server to start
            logger.info(f"Waiting up to {self.timeout} seconds for server on port {appium_port}...")
            start_time = time.time()
            
            while time.time() - start_time < self.timeout:
                # Check if process is still running
                if process.poll() is not None:
                    # Process ended - get error output
                    try:
                        stdout, stderr = process.communicate(timeout=5)
                        stdout_str = stdout.decode('utf-8', errors='ignore') if stdout else ""
                        stderr_str = stderr.decode('utf-8', errors='ignore') if stderr else ""
                        error_msg = f"Appium process ended unexpectedly.\nSTDOUT: {stdout_str}\nSTDERR: {stderr_str}"
                        logger.error(error_msg)
                        return {"success": False, "message": error_msg}
                    except subprocess.TimeoutExpired:
                        return {"success": False, "message": "Process ended and couldn't get output"}
                
                # Check if server is responding
                if self.is_appium_server_running(appium_port):
                    self.servers[appium_port] = process
                    logger.info(f"✅ Successfully started Appium server for {device_id} on port {appium_port}")
                    return {
                        "success": True,
                        "message": f"Appium server started for {device_id}",
                        "port": appium_port,
                        "server_url": f"http://127.0.0.1:{appium_port}"
                    }
                
                # Log progress every 10 seconds
                elapsed = time.time() - start_time
                if elapsed % 10 < 2:
                    logger.info(f"Still waiting for server on port {appium_port}... ({elapsed:.1f}s elapsed)")
                
                time.sleep(2)
            
            # Timeout - cleanup
            logger.warning(f"Timeout waiting for server on port {appium_port}")
            try:
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
            except Exception as e:
                logger.error(f"Error terminating process: {e}")
            
            return {"success": False, "message": f"Timeout starting server for {device_id} (waited {self.timeout}s)"}
            
        except Exception as e:
            logger.error(f"Exception starting server for {device_id}: {e}")
            return {"success": False, "message": f"Exception: {str(e)}"}

    def start_servers_for_devices(self, device_ids: List[str], max_workers: int = 3) -> Dict[str, Any]:
        """Khởi động Appium servers cho multiple devices song song"""
        try:
            logger.info(f"Starting Appium servers for {len(device_ids)} devices with {max_workers} workers")
            results = {}
            
            # Use lower concurrency to avoid overwhelming system
            actual_workers = min(max_workers, len(device_ids))
            
            with ThreadPoolExecutor(max_workers=actual_workers) as executor:
                # Submit tasks
                futures = {
                    executor.submit(self.start_server_for_device, device_id): device_id 
                    for device_id in device_ids
                }
                
                # Collect results
                for future in as_completed(futures):
                    device_id = futures[future]
                    try:
                        result = future.result()
                        results[device_id] = result
                        if result.get("success", False):
                            logger.info(f"✅ {device_id} → Port {result.get('port')}")
                        else:
                            logger.error(f"❌ {device_id} → {result.get('message', 'Unknown error')}")
                    except Exception as e:
                        results[device_id] = {"success": False, "error": str(e)}
                        logger.error(f"❌ {device_id} → Exception: {str(e)}")
            
            successful = sum(1 for r in results.values() if r.get("success", False))
            
            if successful > 0:
                self.is_running = True
            
            logger.info(f"Server startup completed: {successful}/{len(device_ids)} successful")
            
            return {
                "success": successful > 0,
                "message": f"Started {successful}/{len(device_ids)} Appium servers",
                "results": results,
                "total_started": successful
            }
            
        except Exception as e:
            logger.error(f"Error starting servers: {e}")
            return {"success": False, "message": f"Error: {str(e)}"}

    def stop_server_for_device(self, device_id: str) -> Dict[str, Any]:
        """Dừng Appium server cho device cụ thể"""
        try:
            appium_port = self.get_appium_port_for_device(device_id)
            if not appium_port:
                return {"success": False, "message": f"No port mapping for device {device_id}"}
            
            if appium_port in self.servers:
                process = self.servers[appium_port]
                try:
                    process.terminate()
                    process.wait(timeout=5)
                    logger.info(f"Stopped Appium server for {device_id} on port {appium_port}")
                except subprocess.TimeoutExpired:
                    process.kill()
                    logger.info(f"Killed Appium server for {device_id} on port {appium_port}")
                del self.servers[appium_port]
            
            # Force kill any remaining processes on port
            self._kill_process_on_port(appium_port)
            
            return {"success": True, "message": f"Stopped server for {device_id}"}
            
        except Exception as e:
            logger.error(f"Error stopping server for {device_id}: {e}")
            return {"success": False, "message": f"Error: {str(e)}"}

    def stop_all_servers(self) -> Dict[str, Any]:
        """Dừng tất cả Appium servers"""
        try:
            stopped_count = 0
            
            for port, process in list(self.servers.items()):
                try:
                    process.terminate()
                    try:
                        process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        process.kill()
                    stopped_count += 1
                    logger.info(f"Stopped Appium server on port {port}")
                except Exception as e:
                    logger.error(f"Error stopping server on port {port}: {e}")
            
            self.servers.clear()
            
            # Force kill all node processes (nuclear option)
            try:
                subprocess.run(["taskkill", "/F", "/IM", "node.exe"], capture_output=True)
                logger.info("Killed all node.exe processes")
            except Exception:
                pass
            
            self.is_running = False
            return {"success": True, "message": f"Stopped {stopped_count} Appium servers"}
            
        except Exception as e:
            logger.error(f"Error stopping all servers: {e}")
            return {"success": False, "message": f"Error: {str(e)}"}

    def _kill_process_on_port(self, port: int):
        """Kill process đang sử dụng port"""
        try:
            if os.name == 'nt':  # Windows
                # Find process using port
                cmd = f'netstat -ano | findstr :{port}'
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                
                for line in result.stdout.split('\n'):
                    if f':{port}' in line and 'LISTENING' in line:
                        parts = line.split()
                        if len(parts) >= 5:
                            pid = parts[-1]
                            kill_result = subprocess.run(['taskkill', '/F', '/PID', pid], capture_output=True)
                            if kill_result.returncode == 0:
                                logger.info(f"Killed process {pid} on port {port}")
                            break
        except Exception as e:
            logger.error(f"Error killing process on port {port}: {e}")

    def get_server_status(self) -> Dict[str, Any]:
        """Lấy status của tất cả servers"""
        try:
            running_servers = []
            
            for port, process in self.servers.items():
                if process.poll() is None and self.is_appium_server_running(port):
                    running_servers.append({
                        "port": port,
                        "url": f"http://127.0.0.1:{port}",
                        "status": "running",
                        "pid": process.pid
                    })
            
            status_info = {
                "total_servers": len(self.servers),
                "running_servers": running_servers,
                "port_mapping": self.port_mapping,
                "is_running": self.is_running
            }
            
            return {"success": True, "status": status_info}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_device_server_url(self, device_id: str) -> Optional[str]:
        """Lấy server URL cho device cụ thể"""
        appium_port = self.get_appium_port_for_device(device_id)
        if appium_port and appium_port in self.servers:
            process = self.servers[appium_port]
            if process.poll() is None:  # Process still running
                return f"http://127.0.0.1:{appium_port}"
        return None
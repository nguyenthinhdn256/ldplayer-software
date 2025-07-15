import subprocess
import logging
import os
from typing import Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger(__name__)

class ApkManager:
    def __init__(self):
        self.app_mapping = {
            "adbchangelanguage": "et.sanapeli.adbchangelanguag",
            "fbkatana": "com.facebook.katana", 
            "app-deviceinfohw": "ru.andr7e.deviceinfohw",
            "mess": "com.facebook.orca"
        }
    
    def get_connected_devices(self) -> List[str]:
        try:
            result = subprocess.run(["adb", "devices"], capture_output=True, text=True, timeout=10)
            devices = []
            for line in result.stdout.strip().split('\n')[1:]:
                if line.strip() and '\t' in line:
                    device_id, status = line.strip().split('\t')
                    if status == 'device':
                        devices.append(device_id)
            return devices
        except:
            return []
    
    def process_single_device(self, device_id: str, apk_folder: str) -> Dict[str, any]:
        """Xử lý một device"""
        device_results = {"device": device_id, "apps": []}
        
        for app_name, package_name in self.app_mapping.items():
            apk_path = os.path.join(apk_folder, f"{app_name}.apk")
            
            if not os.path.exists(apk_path):
                device_results["apps"].append({
                    "app": app_name,
                    "success": False,
                    "message": f"APK file not found: {apk_path}"
                })
                continue
            
            try:
                # Check if installed
                check_cmd = ["adb", "-s", device_id, "shell", "pm", "list", "packages", package_name]
                check_result = subprocess.run(check_cmd, capture_output=True, text=True, timeout=10)
                is_installed = package_name in check_result.stdout
                
                if is_installed:
                    # Uninstall first
                    uninstall_cmd = ["adb", "-s", device_id, "uninstall", package_name]
                    subprocess.run(uninstall_cmd, capture_output=True, text=True, timeout=30)
                
                # Install
                install_cmd = ["adb", "-s", device_id, "install", "-r", apk_path]
                install_result = subprocess.run(install_cmd, capture_output=True, text=True, timeout=60)
                
                if install_result.returncode == 0 and "Success" in install_result.stdout:
                    action = "Reinstalled" if is_installed else "Installed"
                    device_results["apps"].append({
                        "app": app_name,
                        "success": True,
                        "message": f"{action} successfully"
                    })
                else:
                    device_results["apps"].append({
                        "app": app_name,
                        "success": False,
                        "message": f"Install failed: {install_result.stderr or install_result.stdout}"
                    })
            except Exception as e:
                device_results["apps"].append({
                    "app": app_name,
                    "success": False,
                    "message": f"Error: {str(e)}"
                })
        
        return device_results
    
    def process_all_devices(self, apk_folder: str = "apk") -> List[Dict[str, any]]:
        """Xử lý tất cả devices song song"""
        devices = self.get_connected_devices()
        if not devices:
            return [{"success": False, "message": "No devices connected"}]
        
        results = []
        
        # Xử lý song song các device
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(self.process_single_device, device_id, apk_folder) 
                      for device_id in devices]
            
            for future in as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    results.append({"device": "unknown", "error": str(e)})
        
        return results
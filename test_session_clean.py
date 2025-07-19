import uiautomator2 as u2
import time
import random

# Kết nối emulator-5556
d = u2.connect('emulator-5556')

# if d.xpath('//*[@content-desc="Facebook from Meta"]').wait(timeout=10):
#     print("Đã thấy Logo Facebook")
#     time.sleep(1)
#     d.xpath("//android.view.ViewGroup[3]/android.widget.Button[1]").click()

# if d.xpath('//*[@content-desc="Meta logo" or @content-desc="Logo Meta"]').exists:
#     print("Đã thấy Logo Facebook")
#     time.sleep(1)
#     d.xpath('//*[@text="Create new account"] | //android.view.ViewGroup[3]/android.widget.Button[1] | //*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[2]/android.widget.FrameLayout[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.widget.Button[1]').click()

# if d.xpath('//*[@text="Hãy tạo tài khoản để kết nối với bạn bè, người thân và cộng đồng có chung sở thích."]').wait(timeout=10):
#     print("Đã thấy Hãy Tạo Tài Khoản")
#     time.sleep(1)
#     d.xpath("//android.view.ViewGroup[1]/android.widget.Button[1]").click()

# if d(text="Bạn tên gì?").wait(timeout=5):
#     d.xpath('//*[@text="Tiếp"]').click()
# if d.xpath('//*[@resource-id="android:id/button1"]').wait(timeout=5):
#     print("Button SET xuất hiện")
#     time.sleep(1)
#     d.xpath('//*[@resource-id="android:id/button1"]').click()


# if d.xpath('//*[@text="Ngày sinh của bạn là khi nào?"]').wait(timeout=5):
#     print("Ngày sinh của bạn là khi nào?")
#     time.sleep(1)
#     d.xpath('//*[@text="Tiếp"]').click()
#     time.sleep(1)
#     d.xpath('//*[@text="Tiếp"]').click()
#     time.sleep(3)
#     age = random.randint(18, 38)
#     d(className="android.widget.EditText").send_keys(str(age))
#     time.sleep(1)
#     d.xpath('//*[@text="Tiếp"]').click()
#     time.sleep(2)
#     d.xpath('//*[@text="OK"]').click()
    
# if d.xpath('//*[@text="Giới tính của bạn là gì?"]').wait(timeout=5):
#     print("Giới tính của bạn là gì?")
#     gender = random.choice(["Nam", "Nữ"])
#     time.sleep(1)
#     d.xpath(f'//*[@text="{gender}"]').click()
#     time.sleep(1)
#     d.xpath('//*[@text="Tiếp"]').click()
    
# Lấy random họ
with open('dulieu/hoten/Ho.txt', 'r', encoding='utf-8') as f:
    ho_list = [line.strip() for line in f.readlines() if line.strip() and not line.startswith('#')]
    random_ho = random.choice(ho_list)
with open('dulieu/hoten/Ten.txt', 'r', encoding='utf-8') as f:
    ten_list = [line.strip() for line in f.readlines() if line.strip() and not line.startswith('#')]
    random_ten = random.choice(ten_list)    
# if d.xpath('//*[@text="Chọn tên của bạn"]').wait(timeout=5):
#     time.sleep(1)
#     d.xpath('//*[@text="Sử dụng tên khác"]').click()
#     if d(text="Bạn tên gì?").wait(timeout=5):
#         time.sleep(1)
#         d(text="Họ").click()
#         time.sleep(1)
#         d.send_keys(random_ho)
#         time.sleep(1)
#         d(text="Tên").click()
#         time.sleep(1)
#         d.send_keys(random_ten)
#         time.sleep(1)
#         d.xpath('//*[@text="Tiếp"]').click()
#         time.sleep(1)
#         # hoten_done_status = {"stt": stt_display, "trang_thai": "Đã nhập Họ Tên", "ten_may": device_id, "ket_qua": "", "ho": random_ho, "ten": random_ten, "mat_khau": "", "email_sdt": "", "uid": "", "cookie": "", "token": "", "proxy": ""}
#         # self.status_manager.update_device_status(device_index, hoten_done_status, self.table_manager)



if d.xpath('//*[@text="Chọn tên của bạn"]').wait(timeout=5):
    time.sleep(1)
    d.xpath('//*[@text="Sử dụng tên khác"]').click()
    time.sleep(2)
    if d(text="Bạn tên gì?").wait(timeout=5):
        print("Bạn tên gì?")
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
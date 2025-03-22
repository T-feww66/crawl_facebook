import pickle
from time import sleep
import random

def login_fb_by_cookies(cookies_file, driver):
    # Open Facebook
    if "facebook.com" not in driver.current_url:
        driver.get("https://www.facebook.com")
        sleep(random.randint(1, 8))

    print("Đăng nhập bằng cookies nè anh long")
    # đọc cookies từ file có sẳn
    try:
        cookies = pickle.load(open(cookies_file, "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)
        return True
    except FileNotFoundError:
        print("Không tìm thấy file cookies")

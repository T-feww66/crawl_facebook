import pickle
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from utils.driver import create_driver

def send_keys_randomly(element, text):
    """Nhập ký tự vào ô input với độ trễ ngẫu nhiên để tránh bị phát hiện là bot."""
    for char in text:
        element.send_keys(char)
        sleep(random.uniform(0.1, 0.5))


def login_facebook(email, password, driver, save_cookies=True, cookie_path="./data/cookies/my_cookies.pkl"):
    """Hàm đăng nhập Facebook bằng Selenium và lưu cookie nếu cần thiết."""
    driver.get("https://www.facebook.com")
    sleep(5)
    
    try:
        # Tìm các trường nhập liệu
        user_input = driver.find_element(By.ID, "email")
        password_input = driver.find_element(By.ID, "pass")
        
        # Nhập email và mật khẩu với tốc độ ngẫu nhiên
        send_keys_randomly(user_input, email)
        sleep(random.uniform(3, 7))
        send_keys_randomly(password_input, password)
        
        # Gửi biểu mẫu đăng nhập
        password_input.send_keys(Keys.ENTER)
        sleep(4)  # Chờ trang tải
        
        # Lưu cookie nếu được yêu cầu
        if save_cookies:
            pickle.dump(driver.get_cookies(), open(cookie_path, "wb"))
            print(f"Cookies đã được lưu tại: {cookie_path}")
        
    except Exception as e:
        print(f"Lỗi khi đăng nhập: {e}")
    
    finally:
        driver.quit()

# Gọi hàm login
if __name__ == "__main__":
    
    chrome_driver_path = "./chrome_driver/chromedriver.exe"
    driver = create_driver(chrome_driver_path=chrome_driver_path)
    
    login_facebook(email="tthai9123456@gmail.com", password="0123456789099", driver=driver)

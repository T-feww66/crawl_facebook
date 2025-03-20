# import modules
import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

from time import sleep
from load_cookies import login_fb_by_cookies
import random

# Cấu hình trình duyệt
options = Options()
options.add_experimental_option("detach", True)
options.add_argument("--start-maximized")  # Mở full màn hình
options.add_argument("--disable-notifications")  # Tắt thông báo

# Khởi tạo trình duyệt
chrome_driver_path = "./chromedriver.exe"
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)

# File chứa danh sách group_id
file_group_id = "./group_id.csv"
cookies_file = "my_cookies.pkl"


def crawl_post_id(file_group_id, driver):
    """ Crawl danh sách post_id từ group Facebook """
    # Đọc danh sách group_id từ file CSV
    df = pd.read_csv(file_group_id)
    group_ids = df["group_id"].tolist()

    # Danh sách lưu ID bài viết
    post_ids = []

    # Lặp qua từng group để lấy bài viết
    for group_id in group_ids:
        url = f"https://www.facebook.com/groups/{group_id}"
        print(f"Truy cập group {group_id}")

        login_fb_by_cookies(cookies_file=cookies_file, driver=driver)
        driver.get(url)
        
        # # reset sao moi lan lap
        post_links = []

        # Cuộn trang để load thêm bài viết
        for i in range(50):
            print("Kéo xuống lần: ", i)
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            sleep(random.randint(1, 8))

            # Tìm tất cả các thẻ <a> chứa link bài viết
            post_path = "//a[contains(@href, '/posts/')]"
            class_name = "x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx " \
            "xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xkrqix3 x1sur9pj xi81zsa x1s688f"


            try:
                # Chờ đến khi phần tử xuất hiện
                elements = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, post_path))
                    or
                    EC.presence_of_all_elements_located((By.CLASS_NAME, class_name))
                )

                post_links.extend([element.get_attribute("href") for element in elements])       

            except NoSuchElementException:
                print(f"Không tìm thấy element này")
            except StaleElementReferenceException:
                print(f"phần tử thao tác không hợp lệ")

        #lay post tu link va chuyen sang file csv
        if post_links:
            for i, url_post in enumerate(post_links):
                post_id = url_post.split("/")[-2]  # Lấy post_id từ URL
                post_ids.append(
                    {"group_id": group_id, "post_id": post_id, "post_url": url_post})
                print(f"Lấy post thứ {i} có URL")

        else:
            print(f"Không tìm thấy bài viết trong group {group_id}")

        # # Lưu danh sách bài viết vào file CSV
        df_url_posts = pd.DataFrame(post_ids)
        df_url_posts.to_csv("post.csv", index=False)

        print("✅ Đã lấy xong ID bài viết!")


def visit_groups(file_group_id, driver):
    df = pd.read_csv(file_group_id)
    group_ids = df["group_id"].tolist()

    for index, group_id in enumerate(group_ids):
        group_url = f"https://www.facebook.com/groups/{group_id}"
        print(str(index) + "->>>>>>> Truy cập group: ", group_url)

        isLogin = login_fb_by_cookies(cookies_file=cookies_file, driver=driver)
        if isLogin:
            driver.get(group_url)
            sleep(random.randint(1, 8))

# crawl_post_id(file_group_id=file_group_id, driver=driver)
visit_groups(file_group_id=file_group_id, driver=driver)
driver.quit()

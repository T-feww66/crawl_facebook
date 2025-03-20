# import modules
import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException

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
post_file = "./post_data/post_ids_0.csv"
cookies_file = "my_cookies.pkl"
comment_xpath = "//div[@role='article']"


def count_comments(xpath, driver):
    try:
        elements = driver.find_elements(By.XPATH, xpath)
        return len(elements)
    except:
        return 0


def crawl_post_content(driver):

    # Xpath bài viết hoặc bài viết dạng reel
    post_content_xpath_reel = "/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[2]/div/div/div/div/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div/div/div/div[13]/div/div/div[2]/div/div[1]/div/a/div[1]/div[2]/div/div/div[2]/span/div"
    post_content_xpath = '//div[@role="dialog"][@aria-labelledby]//div[@dir="auto"]'

    # xpath nút xem thêm
    see_more_path = "/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[2]/div/div/div/div/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div/div/div/div[13]/div/div/div[2]/div/div[1]/div/a/div[1]/div[2]/div/div/div[2]/span/div/object/div"

    try:
        see_more = WebDriverWait(driver, random.uniform(3, 5)).until(
                EC.presence_of_element_located((By.XPATH, see_more_path)))
        see_more.click()
        sleep(random.uniform(1, 6))
        post_element = WebDriverWait(driver, random.uniform(3, 5)).until(
            EC.presence_of_element_located((By.XPATH, post_content_xpath_reel)))
        return post_element.text
            
    except NoSuchElementException:
        post_element = WebDriverWait(driver, random.uniform(3, 5)).until(
                EC.presence_of_element_located((By.XPATH, post_content_xpath)))
        return post_element.text
    except TimeoutException:
        post_element = WebDriverWait(driver, random.uniform(3, 5)).until(
                EC.presence_of_element_located((By.XPATH, post_content_xpath)))
        return post_element.text



def crawl_comment_by_post_id(post_file, driver):
    """ Crawl danh sách post_id từ group Facebook """
    # Đọc danh sách group_id từ file CSV
    df = pd.read_csv(post_file)

    post_urls = df["post_url"].tolist()
    post_urls = post_urls[:5]

    # Lặp qua từng bài post để lấy comment
    for i, post_url in enumerate(post_urls):

        print("Truy cập bài viết số: ", i)

        isLogin = login_fb_by_cookies(cookies_file=cookies_file, driver=driver)

        if isLogin:
            driver.get(post_url)
            sleep(random.uniform(1, 5))

            post_content = crawl_post_content(driver=driver)

            # # Đếm số lượng comment ban đầu
            # pre_count_comment = count_comments(
            #     xpath=comment_xpath, driver=driver)

            # # Cuộn trang để load thêm bình luận
            # for i in range(10):
            #     comment_elements = driver.find_elements(By.XPATH, comment_xpath)
            #     print("Kéo xuống lần: ", i)

            #     driver.execute_script("arguments[0].scrollIntoView();", comment_elements[-1])
            #     sleep(random.randint(1, 6))

            #     new_count_comments = count_comments(xpath=comment_xpath, driver=driver)

            #     if new_count_comments == pre_count_comment:
            #         print("Đã load toàn bộ bình luận")

        #         # Tìm tất cả các thẻ <a> chứa link bài viết
        #         post_path = "//a[contains(@href, '/posts/')]"
        #         class_name = "x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx " \
        #         "xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xkrqix3 x1sur9pj xi81zsa x1s688f"

        #         try:
        #             # Chờ đến khi phần tử xuất hiện
        #             elements = WebDriverWait(driver, 10).until(
        #                 EC.presence_of_all_elements_located((By.XPATH, post_path))
        #                 or
        #                 EC.presence_of_all_elements_located((By.CLASS_NAME, class_name))
        #             )

        #             post_links.extend([element.get_attribute("href") for element in elements])

        #         except NoSuchElementException:
        #             print(f"Không tìm thấy element này")
        #         except StaleElementReferenceException:
        #             print(f"phần tử thao tác không hợp lệ")

        #     #lay post tu link va chuyen sang file csv
        #     if post_links:
        #         for i, url_post in enumerate(post_links):
        #             post_id = url_post.split("/")[-2]  # Lấy post_id từ URL
        #             post_ids.append(
        #                 {"group_id": group_id, "post_id": post_id, "post_url": url_post})
        #             print(f"Lấy post thứ {i} có URL")

        #     else:
        #         print(f"Không tìm thấy bài viết trong group {group_id}")

        #     # # Lưu danh sách bài viết vào file CSV
        #     df_url_posts = pd.DataFrame(post_ids)
        #     df_url_posts.to_csv("post.csv", index=False)

        #     print("✅ Đã lấy xong ID bài viết!")


crawl_comment_by_post_id(post_file=post_file, driver=driver)
driver.quit()

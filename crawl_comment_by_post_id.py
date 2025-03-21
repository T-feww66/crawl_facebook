# import modules
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException

from time import sleep
from load_cookies import login_fb_by_cookies
from slipt_comments import split_comments
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

# File
post_file = "./post_data/post_ids_1.csv"
cookies_file = "my_cookies.pkl"

# variables
section_comment_xpath = "//div[@role='article']"
# Xpath bài viết hoặc bài viết dạng reel
post_content_xpath_reel = "/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[2]/div/div/div/div/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div/div/div/div[13]/div/div/div[2]/div/div[1]/div/a/div[1]/div[2]/div/div/div[2]/span/div"
post_content_xpath = '//div[@role="dialog"][@aria-labelledby]//div[@dir="auto"]'

# xpath nút xem thêm
see_more_path = "/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[2]/div/div/div/div/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div/div/div/div[13]/div/div/div[2]/div/div[1]/div/a/div[1]/div[2]/div/div/div[2]/span/div/object/div"

# xpath comment
#
comment_xpath = "//div[contains(@class, 'xwib8y2') and contains(@class, 'xn6708d') and contains(@class, 'x1ye3gou') and contains(@class, 'x1y1aw1k')]"

# Hàm này để đếm số lượng element của comments(bình luận)


def count_comments(xpath, driver):
    try:
        elements = driver.find_elements(By.XPATH, xpath)
        return len(elements)
    except:
        return 0

# Hàm này để lấy dữ liệu nội dung của bài viết


def crawl_post_content(driver):
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

    # Khi mà nút xem thên không có
    except TimeoutException:
        post_element = WebDriverWait(driver, random.uniform(3, 5)).until(
            EC.presence_of_element_located((By.XPATH, post_content_xpath)))
        return post_element.text


def crawl_comment_by_post_id(post_file, driver):
    """ Crawl danh sách post_id từ group Facebook """

    # chứa dữ liệu comments
    comments_file = []

    # Đọc danh sách group_id từ file CSV
    df = pd.read_csv(post_file)

    post_urls = df["post_url"].tolist()

    # Lặp qua từng bài post để lấy comment
    for i, post_url in enumerate(post_urls):
        post_id = post_url.split("/")[-2]

        print("Truy cập bài viết số: ", i)

        isLogin = login_fb_by_cookies(cookies_file=cookies_file, driver=driver)

        if isLogin:
            driver.get(post_url)
            sleep(random.uniform(1, 5))

            post_content = crawl_post_content(driver=driver)

            # Cuộn trang để load thêm bình luận
            for i in range(10):

                # Đếm số lượng comment ban đầu
                pre_count_comment = count_comments(
                    xpath=section_comment_xpath, driver=driver)

                comment_elements = driver.find_elements(
                    By.XPATH, section_comment_xpath)
                print("Kéo xuống lần: ", i)

                driver.execute_script(
                    "arguments[0].scrollIntoView();", comment_elements[-1])
                sleep(random.randint(1, 6))

                new_count_comments = count_comments(
                    xpath=section_comment_xpath, driver=driver)

                if new_count_comments == pre_count_comment:
                    print("Đã load toàn bộ bình luận")
                    sleep(random.uniform(1, 4))
                    break

            print("Lấy dữ liệu nè anh long: ")
            # tìm tất cả nút xem thêm trong phần bình luận
            try:
                comment_see_more_xpath = "//div[contains(@class, 'xwib8y2') and contains(@class, 'xn6708d') and contains(@class, 'x1ye3gou') and contains(@class, 'x1y1aw1k')]//div[@role='button']"
                see_more_comments = driver.find_elements(
                    By.XPATH, comment_see_more_xpath)

                for see_more_comment in see_more_comments:
                    see_more_comment.click()

            except NoSuchElementException:
                print("Bài viết này không có bình luận dài")
                continue
            except ElementClickInterceptedException:
                print("Khi nút xem thêm bị che khuất")
                continue

            # lấy các bình luận phía ngoài cùng của bài viết
            comments = [comment.text for comment in driver.find_elements(
                By.XPATH, comment_xpath)]
            comments = comments[1:-1]
            for i_comment, comment in enumerate(comments):
                print(f"Lấy comment thứ {i_comment}")
                comments_file.append(
                    {"post_id": post_id, "post_content": post_content, "comment": comment})
        else:
            driver.quit()
    # # Lưu danh sách bài viết vào file CSV
    df_comment = pd.DataFrame(comments_file)
    df_comment = split_comments(df_comment)
    df_comment.to_csv("./comments_data/datacomment_0.csv", index=False)


crawl_comment_by_post_id(post_file=post_file, driver=driver)
driver.quit()

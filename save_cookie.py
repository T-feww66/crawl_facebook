import pickle
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from time import sleep

#Khởi tạo driver
options = Options()
options.add_experimental_option("detach", True)

service = Service("./chromedriver.exe")

driver = webdriver.Chrome(service=service, options=options)

#get trang web
driver.get("https://www.facebook.com")


sleep(5)
user_input = driver.find_element(By.ID, "email")
password = driver.find_element(By.ID, "pass")

sleep(5)
user_input.send_keys("tthai9123456@gmail.com")
sleep(5)
password.send_keys("0123456789099")

password.send_keys(Keys.ENTER)

sleep(5)

pickle.dump(driver.get_cookies(), open("my_cookies.pkl", "wb"))
driver.close()
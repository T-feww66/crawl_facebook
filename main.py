import pandas as pd
from scrapers.crawl_comment_by_post_id import crawl_comment_by_post_id
from utils.driver import create_driver
from utils.slipt_comments import split_comments


# File
post_file = "./data/posts/post_ids_9.csv"
cookies_file = "./data/cookies/my_cookies.pkl"
chrome_driver_path = "./chrome_driver/chromedriver.exe"



driver = create_driver(chrome_driver_path=chrome_driver_path)
list_comments = crawl_comment_by_post_id(post_file=post_file, cookies_file=cookies_file, driver=driver)


# # Lưu danh sách bài viết vào file CSV
df_comment = pd.DataFrame(list_comments)
df_comment = split_comments(df_comment)
print("Lưu comment.csv")
df_comment.to_csv("./data/comments/datacomment_9.csv", index=False)
driver.quit()
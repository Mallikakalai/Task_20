import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

paths = r"D:\Downloads\chromedriver-win64\chromedriver.exe"
os.environ["PATH"] += os.pathsep + os.path.dirname(paths)

chrome_options = (Options())
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://labour.gov.in/")
driver.maximize_window()
time.sleep(3)

documents_menu = driver.find_element(By.LINK_TEXT,"Documents")
actions = ActionChains(driver)
actions.move_to_element(documents_menu).perform()
time.sleep(3)

monthly_report_link = driver.find_element(By.LINK_TEXT, "Monthly Progress Report")
url=monthly_report_link.get_attribute('href')
monthly_report_link.click()

##downloading latest monthly report
latest_report=driver.find_element(By.LINK_TEXT,"Download(139.61 KB)")
latest_report_url=latest_report.get_attribute('href')
latest_report.click()
j=driver.switch_to.alert
j.accept()

report_response = requests.get(latest_report_url)
with open(r"D:\Python_HW\Task_Downloads\Monthly_Progress_Report.pdf", 'wb') as file:
    file.write(report_response.content)

print("Monthly Progress Report downloaded successfully.")

#Opening Media menu and navigate photo gallery

media_menu = driver.find_element(By.LINK_TEXT,"Media")
media_menu.click()
driver.find_element(By.LINK_TEXT,"Click for more info of Press Releases").click()
driver.find_element(By.LINK_TEXT,"Photo Gallery").click()
time.sleep(5)

#create a folder and store the photos
photo_folder=r"D:\Python_HW\Photo_Folder"
if not os.path.exists(photo_folder):
     os.makedirs(photo_folder)

#dowonload the first 10 photos
photos = driver.find_elements(By.CSS_SELECTOR, "img")[:10]

for index, photo in enumerate(photos):
    photo_url = photo.get_attribute('src')
    photo_response = requests.get(photo_url)
    with open(os.path.join(photo_folder, f"photo_{index + 1}.jpg"), 'wb') as file:
        file.write(photo_response.content)
    print(f"Downloaded photo {index + 1}")

print("Photos downloaded successfully.")



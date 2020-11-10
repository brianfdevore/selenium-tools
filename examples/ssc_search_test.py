from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import csv

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get("https://www.skidsteercabs.com")

search = driver.find_element_by_name("q")
search.send_keys("heater")
search.send_keys(Keys.RETURN)

try:
    results = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "grid"))
    )
    dataList = []
    items = results.find_elements_by_class_name("four-fifths")
    for item in items:
        h3 = item.find_element_by_tag_name("h3")
        a = h3.find_element_by_tag_name("a")
        itemProps = [a.text, a.get_attribute("href")]
        dataList.append(itemProps)

    with open('ssc_search_results.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(dataList)

finally:
    driver.quit()


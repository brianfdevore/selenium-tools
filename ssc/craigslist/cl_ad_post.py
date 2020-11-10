from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
import os.path


def find(browser):
    add_images = browser.find_element_by_xpath('//input[@name="file"]')
    if add_images:
        return add_images
    else:
        return False

# init browser and navigate to Craigslist
browser = webdriver.Chrome('C:\Program Files (x86)\chromedriver.exe')
browser.get('https://post.craigslist.org/')

# select post location
browser.find_element_by_class_name('ui-selectmenu-text').click()
browser.find_element_by_xpath('//li[@id="ui-id-28"]').click()
browser.find_element_by_xpath('//button[@name="go"]').click()


# post type page
browser.find_element_by_xpath('//input[@name="id" and @value="fsd"]').click()

# category
browser.find_element_by_xpath('//input[@name="id" and @value="194"]').click()

# main post page
title_area = browser.find_element_by_xpath('//input[@name="PostingTitle" and @id="PostingTitle"]')
title_area.send_keys('SkidSteerCabs.com | Skid Steer Cab Enclosures & Attachments')
city = browser.find_element_by_xpath('//input[@name="geographic_area" and @id="geographic_area"]')
city.send_keys('Frostburg, MD')
postal_code = browser.find_element_by_xpath('//input[@name="postal" and @id="postal_code"]')
postal_code.send_keys(21532)
time.sleep(1)

# main text section | HTML formatting is okay here (https://www.craigslist.org/about/help/html_in_craigslist_postings/details)
main_text = browser.find_element_by_xpath('//textarea[@name="PostingBody" and @id="PostingBody"]')
main_text.send_keys("<h1>SkidSteerCabs.com</h1>")
main_text.send_keys(Keys.ENTER)
main_text.send_keys(Keys.ENTER)
main_text.send_keys("Visist our website to view products and pricing at: <a href='https://www.skidsteercabs.com'>www.skidsteercabs.com</a>")
main_text.send_keys(Keys.ENTER)
main_text.send_keys(Keys.ENTER)
main_text.send_keys('You can also give us a call at (888) 497-8898 or click the chat button on our home page to talk to a real human right now.')
main_text.send_keys(Keys.ENTER)
main_text.send_keys(Keys.ENTER)
main_text.send_keys("We have cab enclosure kits, polycarbonate replacement slugs for your door glass, a full line of attchments, heaters, wipers, and more!")
main_text.send_keys(Keys.ENTER)
main_text.send_keys(Keys.ENTER)
main_text.send_keys('If you need help getting warm and dry, increasing operator safety, or finding the right attachment to boost productivity for your skid steer, we have got what you need!')
main_text.send_keys(Keys.ENTER)
main_text.send_keys(Keys.ENTER)
main_text.send_keys("Give us a call today for pricing and availability for your machine: (888) 497-8898")

# price
price = browser.find_element_by_xpath('//input[@name="price"]')
price.send_keys(1299)

# make/manufacturer
make = browser.find_element_by_xpath('//input[@name="sale_manufacturer"]')
make.send_keys('All')

# model name/number
model = browser.find_element_by_xpath('//input[@name="sale_model"]')
model.send_keys('All')

# size/dimensions
size = browser.find_element_by_xpath('//input[@name="sale_size"]')
size.send_keys('All')

# # condition (choose "New", which is first menu option)
# condition = browser.find_element_by_xpath('//span[@id="ui-selectmenu-button"]').click()

# actions = ActionChains(browser)

# for x in range(1):
#     actions.send_keys(Keys.ARROW_DOWN)
# actions.send_keys(Keys.ENTER).click()
# actions.perform()

# condition
condition = browser.find_element_by_xpath('//span[@id="ui-id-2-button"]').click()
browser.find_element_by_xpath('//li[@id="ui-id-4"]').click()

# email
email = browser.find_element_by_xpath('//input[@name="FromEMail"]')
email.send_keys('sales@skidsteercabs.com')

# continue button
browser.find_element_by_xpath('//button[@name="go" and @value="continue"]').click()

# continue button
location_submit1 = browser.find_element_by_xpath('//button[@class="continue bigbutton"]').click()

# continue button (keep old area?)
try:
    location_submit2 = browser.find_element_by_xpath('//button[@class="continue medium-pickbutton" and @name="keep_old_area"]').click()
except:
    print("Error")
finally:
    # send images (using classic image upload link)
    browser.find_element_by_xpath('//a[@id="classic"]').click()
    add_images = browser.find_element_by_xpath('//input[@name="file"]')

img = []
path = 'images'
valid_image = ['.jpg', '.gif', '.png', '.tga']
for f in os.listdir(path):
    ext = os.path.splitext(f)[1]
    if ext.lower() not in valid_image:
        continue
    print(f)
    img.append(f'/images/{f}')

for i in sorted(img):
    if add_images != False:
        print(os.getcwd() + i)
        add_images.send_keys(os.getcwd() + i)
        add_images = WebDriverWait(browser, 3).until(find)
    else:
        continue

# done with images button
browser.find_element_by_xpath('//button[@value="Done with Images"]').click()

# publish button (last step, commits purchase)
# browser.find_element_by_xpath('//button[@value="Continue"]').click()
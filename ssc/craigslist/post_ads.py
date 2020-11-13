from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
import os.path
import json
import click


def find(browser):
    add_images = browser.find_element_by_xpath('//input[@name="file"]')
    if add_images:
        return add_images
    else:
        return False

def do_browser_init():
    # init browser and navigate to Craigslist
    driver = webdriver.Chrome('..\\..\\chromedriver.exe')
    driver.get('https://post.craigslist.org/')
    return driver

def confirm_proceed():
    config = get_config()
    states_regions_dict = get_states_regions()
        
    # iterate through post_states, and nested regions to post an ad for each
    if len(config['post_states']) > 0:
        # get count for states/regions where ads will be created
        cnt = 0
        for state in config['post_states']:
            for region in states_regions_dict[state].items():
                cnt += 1

        print('\nYou are attempting to post %s ads in the regions below:\n' % cnt)

        # print list of states/regions where ads will be created
        for state in config['post_states']:
            print('[' + state + ']')
            for region in states_regions_dict[state].items():
                print('%s' % region[0])
            print('\n')        

        # prompt the user to confirm we should proceed
        if click.confirm('Do you want to proceed and post ' + str(cnt) + ' ads?', default=True):
            return True
        else:
            return False
        
    else:
        print('Error: no states specified in ad_config.json file.')
        time.sleep(2)
        exit()


def get_config():
    # open ad_config.json file to load configs for use in ad fields
    with open('.\\infiles\\ad_config.json') as f1:
        conf_data = json.load(f1)
        return conf_data

def get_states_regions():
    # open regions_from_cl_us_by_state.json file to load states/regions info
    with open('.\\outfiles\\regions_from_cl_us_by_state.json') as f2:
        sr_dict = json.load(f2)
        return sr_dict

def post_ads():
    config = get_config()
    states_regions_dict = get_states_regions()
        
    # iterate through post_states, and nested regions to post an ad for each
    for state in config['post_states']:
        for region, ui_id in states_regions_dict[state].items():
            print('Posting ad in: [%s] [%s]' % (region, state))    
            browser = do_browser_init()   
    
            # post location
            browser.find_element_by_class_name('ui-selectmenu-text').click()
            #browser.find_element_by_xpath('//li[@id="ui-id-28"]').click()
            browser.find_element_by_xpath("//li[@id='" + ui_id + "']").click()
            browser.find_element_by_xpath('//button[@name="go"]').click()


            # post type (For Sale By Dealer = fsd, For Sale By Owner = fso)
            browser.find_element_by_xpath("//input[@name='id' and @value='" + config['post_type'] + "']").click()
            #browser.find_element_by_xpath('//input[@name="id" and @value="fso"]').click()

            # post category
            browser.find_element_by_xpath("//input[@name='id' and @value='" + config['post_category'] + "']").click()
            #browser.find_element_by_xpath('//input[@name="id" and @value="178"]').click()

            # main post page
            title_area = browser.find_element_by_xpath('//input[@name="PostingTitle" and @id="PostingTitle"]')
            title_area.send_keys(config['post_title'])
            city = browser.find_element_by_xpath('//input[@name="geographic_area" and @id="geographic_area"]')
            city.send_keys(config['post_city'])
            postal_code = browser.find_element_by_xpath('//input[@name="postal" and @id="postal_code"]')
            postal_code.send_keys(int(config['postal_code']))
            time.sleep(1)

            # main text section | HTML markup is okay here (https://www.craigslist.org/about/help/html_in_craigslist_postings/details)
            main_text = browser.find_element_by_xpath('//textarea[@name="PostingBody" and @id="PostingBody"]')

            # open main_text.html file and send that text into the main text field
            with open('.\\infiles\\main_text.html', encoding="utf8") as f:
                lines = f.readlines()
                for line in lines:
                    main_text.send_keys(line)

            # another way to do it...
            # main_text.send_keys("<h1>SkidSteerCabs.com</h1>")
            # main_text.send_keys(Keys.ENTER)
            # main_text.send_keys(Keys.ENTER)
            # main_text.send_keys("Visist our website to view products and pricing at: <a href='https://www.skidsteercabs.com'>www.skidsteercabs.com</a>")
            # main_text.send_keys(Keys.ENTER)
            # main_text.send_keys(Keys.ENTER)
            # main_text.send_keys('You can also give us a call at (888) 497-8898 or click the chat button on our home page to talk to a real human right now.')
            # main_text.send_keys(Keys.ENTER)
            # main_text.send_keys(Keys.ENTER)
            # main_text.send_keys("We have cab enclosure kits, polycarbonate replacement slugs for your door glass, a full line of attchments, heaters, wipers, and more!")
            # main_text.send_keys(Keys.ENTER)
            # main_text.send_keys(Keys.ENTER)
            # main_text.send_keys('If you need help getting warm and dry, increasing operator safety, or finding the right attachment to boost productivity for your skid steer, we have got what you need!')
            # main_text.send_keys(Keys.ENTER)
            # main_text.send_keys(Keys.ENTER)
            # main_text.send_keys("Give us a call today for pricing and availability for your machine: (888) 497-8898")

            # price
            price = browser.find_element_by_xpath('//input[@name="price"]')
            price.send_keys(int(config['post_price']))

            # make/manufacturer
            make = browser.find_element_by_xpath('//input[@name="sale_manufacturer"]')
            make.send_keys(config['he_manufacturer'])

            # model name/number
            model = browser.find_element_by_xpath('//input[@name="sale_model"]')
            model.send_keys(config['he_model'])

            # size/dimensions
            size = browser.find_element_by_xpath('//input[@name="sale_size"]')
            size.send_keys(config['he_size'])
            
            # condition
            browser.find_element_by_xpath('//span[@id="ui-id-2-button"]').click()
            browser.find_element_by_xpath('//li[@id="ui-id-4"]').click()

            # email
            email = browser.find_element_by_xpath('//input[@name="FromEMail"]')
            email.send_keys(config['post_email'])

            # continue button
            browser.find_element_by_xpath('//button[@name="go" and @value="continue"]').click()

            # continue button
            browser.find_element_by_xpath('//button[@class="continue bigbutton"]').click()

            # continue button (in case we are prompted to keep old location/area, and need to choose one of the 2 options)
            try:
                browser.find_element_by_xpath('//button[@class="continue medium-pickbutton" and @name="keep_old_area"]').click()
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

            # publish button (last step for ad creation, commits purchase)
            browser.find_element_by_xpath('//button[@value="Continue"]').click()

            # close the browser instance
            browser.quit()


def main():
    if confirm_proceed():
        post_ads()
    else:
        print('Job cancelled...')
        time.sleep(1.5)
        exit()

if __name__ == "__main__":
    main()
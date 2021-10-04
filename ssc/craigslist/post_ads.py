from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
import os.path
import json
import click
import boto3
import logging

# Create a custom logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create handlers for the custom logger
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler('post_ads.log', mode="a")
c_handler.setLevel(logging.WARNING)
f_handler.setLevel(logging.DEBUG)

# Create formatters and add them to the handlers
c_format = logging.Formatter('%(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)

def find(browser):
    add_images = browser.find_element_by_xpath('//input[@name="file"]')
    if add_images:
        return add_images
    else:
        return False

def do_browser_init():
    # init browser and navigate to Craigslist, login and send to post page
    driver = webdriver.Chrome('..\\..\\chromedriver.exe')

    # do login
    creds = get_account_creds()
    driver.get('https://accounts.craigslist.org/login/home')
    username = driver.find_element_by_xpath("//input[@id='inputEmailHandle']")
    username.send_keys(creds['username'])
    password = driver.find_element_by_xpath("//input[@id='inputPassword']")
    password.send_keys(creds['password'])
    driver.find_element_by_xpath('//button[@id="login"]').click()
    time.sleep(2)
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

def get_account_creds():
    session = boto3.Session(profile_name='bdc')
    client = session.client('ssm')
    uname = client.get_parameter(
        Name = '/apps/craigslist/accounts/ssc1/username'
    )
    pwd = client.get_parameter(
        Name = '/apps/craigslist/accounts/ssc1/password',
        WithDecryption=True
    )

    creds = { 
        'username' : uname['Parameter']['Value'],
        'password' : pwd['Parameter']['Value']
     }

    return creds

def get_payment_info():
    config = get_config()
    session = boto3.Session(profile_name=str(config['aws_profile']))
    client = session.client('ssm')
    num = client.get_parameter(
        Name = '/payment_cards/' + str(config['pymt_card_code']) + '/card_number',
        WithDecryption=True
    )
    exp = client.get_parameter(
        Name = '/payment_cards/' + str(config['pymt_card_code']) + '/expiration',
        WithDecryption=True
    )

    cvv = client.get_parameter(
        Name = '/payment_cards/' + str(config['pymt_card_code']) + '/cvv',
        WithDecryption=True
    )

    add = client.get_parameter(
        Name = '/payment_cards/' + str(config['pymt_card_code']) + '/address',
        WithDecryption=True
    )

    first = client.get_parameter(
        Name = '/payment_cards/' + str(config['pymt_card_code']) + '/first_name',
        WithDecryption=True
    )

    last = client.get_parameter(
        Name = '/payment_cards/' + str(config['pymt_card_code']) + '/last_name',
        WithDecryption=True
    )

    city = client.get_parameter(
        Name = '/payment_cards/' + str(config['pymt_card_code']) + '/city',
        WithDecryption=True
    )

    state = client.get_parameter(
        Name = '/payment_cards/' + str(config['pymt_card_code']) + '/state',
        WithDecryption=True
    )

    zip = client.get_parameter(
        Name = '/payment_cards/' + str(config['pymt_card_code']) + '/zip',
        WithDecryption=True
    )

    params = { 
        'card_number' : num['Parameter']['Value'],
        'expiration_date' : exp['Parameter']['Value'],
        'cvv' : cvv['Parameter']['Value'],
        'address' : add['Parameter']['Value'],
        'first_name' : first['Parameter']['Value'],
        'last_name' : last['Parameter']['Value'],
        'city' : city['Parameter']['Value'],
        'state' : state['Parameter']['Value'],
        'zip_code' : zip['Parameter']['Value'],
     }

    return params

def post_ads():
    config = get_config()
    states_regions_dict = get_states_regions()

    # check to make sure there are states specified in config file
    if not config['post_states']:
        logger.error('No states were specified in the ad_config.json configuration file, terminating program.')
        exit()

    # iterate through post_states and nested regions to post an ad for each
    logger.debug('## SESSION START ##')
    for state in config['post_states']:
        logger.debug('STARTING ' + state.upper())
        for region, ui_id in states_regions_dict[state].items():
            try:
                logger.debug('Posting ad in: [%s] [%s]' % (region, state))    
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

                # show my phone number
                browser.find_element_by_xpath('//input[@name="show_phone_ok"]').click()

                # phone calls OK
                browser.find_element_by_xpath('//input[@name="contact_phone_ok"]').click()

                # text/sms OK
                browser.find_element_by_xpath('//input[@name="contact_text_ok"]').click()
                time.sleep(0.5)

                # phone number
                phone = browser.find_element_by_xpath('//input[@name="contact_phone"]')
                phone.send_keys(config['contact_phone'])  #<-- failing here with "NoneType object has no attribute 'send keys'", when .click() is used

                # contact name
                contact = browser.find_element_by_xpath('//input[@name="contact_name"]')
                contact.send_keys(config['contact_name']) #<-- failing here with "NoneType object has no attribute 'send keys'", when .click() is used

                # email
                #email = browser.find_element_by_xpath('//input[@name="FromEMail"]')
                #email.send_keys(config['post_email'])

                # continue button
                browser.find_element_by_xpath('//button[@name="go" and @value="continue"]').click()

                # continue button (not present on all flows such as for Canberra CT)
                try:
                    browser.find_element_by_xpath('//button[@class="continue bigbutton"]').click()
                except Exception:
                    logger.debug("Exception occurred while attempting to find Continue button (line 290).")

                # continue button (in case we are prompted to keep old location/area, and need to choose one of the 2 options)
                try:
                    browser.find_element_by_xpath('//button[@class="continue medium-pickbutton" and @name="keep_old_area"]').click()
                except Exception:
                    logger.debug("Area button not found (line 298)")

                # send images (using classic image upload link)
                time.sleep(0.5)
                logger.debug('Beginning image uploads')
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

                logger.debug('Image uploads completed')

                # done with images button
                browser.find_element_by_xpath('//button[@value="Done with Images"]').click()

                # publish button (last step for ad creation, commits purchase)
                browser.find_element_by_xpath('//button[@value="Continue"]').click()
                
                # click the continue button to proceed with payment for the post
                # browser.find_element_by_xpath('//button[@name="go"]').click() 

                # submit the payment card info on the payment page
                logger.debug('Beginning payment submission')
                card = get_payment_info()
                f_name = browser.find_element_by_xpath('//input[@id="cardFirstName"]')
                f_name.send_keys(card['first_name'])
                l_name = browser.find_element_by_xpath('//input[@id="cardLastName"]')
                l_name.send_keys(card['last_name'])
                number = browser.find_element_by_xpath('//input[@id="cardNumber"]')
                number.send_keys(card['card_number'])
                exp_date = browser.find_element_by_xpath('//input[@id="expDate"]')
                exp_date.send_keys(card['expiration_date'])
                cvv = browser.find_element_by_xpath('//input[@id="cvNumber"]')
                cvv.send_keys(card['cvv'])
                address = browser.find_element_by_xpath('//input[@name="cardAddress"]')
                address.send_keys(card['address'])
                zip = browser.find_element_by_xpath('//input[@id="cardPostal"]')
                zip.send_keys(card['zip_code'])
                # city = browser.find_element_by_xpath('//input[@id="cardCity"]')
                # city.send_keys(card['city'])
                # state = browser.find_element_by_xpath('//input[@id="cardState"]')
                # state.send_keys(card['state'])
                time.sleep(1)
                browser.find_element_by_xpath('//button[@id="submitter"]').click()
                time.sleep(10)
                logger.debug('Payment submitted and ad published')

                # close the browser instance
                browser.quit()
                logger.debug('Browser closed, successful post in: [%s] [%s]' % (region, state))

            except Exception:
                logger.exception("Exception occurred:")
                browser.quit()   

def main():
    if confirm_proceed():
        post_ads()
    else:
        logger.info('Job cancelled by user.')
        time.sleep(1.5)
        exit()

if __name__ == "__main__":
    main()
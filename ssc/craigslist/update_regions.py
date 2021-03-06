from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
import os.path
import json
import csv


def find(browser):
    add_images = browser.find_element_by_xpath('//input[@name="file"]')
    if add_images:
        return add_images
    else:
        return False

# init browser and navigate to Craigslist
browser = webdriver.Chrome('..\\..\\chromedriver.exe')
browser.get('https://post.craigslist.org/')

# # find all post location/region options (gets select list and ids) - this is working code, but doesn't give the ids needed to post
# select = Select(browser.find_element_by_id('ui-id-1'))
# dataList = []
# dataDict = {}
# print('Craigslist regions count: ', len(select.options))
# for region in select.options:
#     itemProps = [region.get_attribute('text'), region.get_attribute('value')]
#     dataList.append(itemProps)
#     dataDict[region.get_attribute('text')] = region.get_attribute('value')
    
# # create 2 column csv file with all regions found
# with open('.\\outfiles\\regions_from_cl_raw.csv', 'w', newline='') as f1:
#     writer = csv.writer(f1)
#     writer.writerows(dataList)

# # create json file with all regions found
# with open('.\\outfiles\\regions_from_cl_raw.json', 'w') as f2:
#     regions = {}
#     regions['regions'] = dataDict
#     json.dump(regions, f2)

# browser.quit()


# find all post location options (gets ul and li's) - this option is needed to post ads since it gets the id for each li 
browser.find_element_by_class_name('ui-selectmenu-text').click()
li_options = browser.find_elements_by_xpath('//li[@class="ui-menu-item"]')

dataList = []
dataDict = {}
print('Craigslist regions count: ', len(li_options))
for region in li_options:
    itemProps = [region.text, region.get_attribute('id')]
    dataList.append(itemProps)
    dataDict[region.text] = region.get_attribute('id')
    
# create 2 column csv file with all regions found
with open('.\\outfiles\\regions_from_cl_raw.csv', 'w', newline='') as f1:
    writer = csv.writer(f1)
    writer.writerows(dataList)

# create json file with all regions found
with open('.\\outfiles\\regions_from_cl_raw.json', 'w') as f2:
    regions = {}
    regions['regions'] = dataDict
    json.dump(regions, f2)

browser.quit()


### process regions ###

# open the Craigslist regions file generated by update_regions.py in this project
with open('.\\outfiles\\regions_from_cl_raw.json') as f1:
    cl_regions = json.load(f1)

# open the static us states file in this project
with open('.\\infiles\\us_states_list.json') as f2:
    states = json.load(f2)

# find the regions for each state
cities = {}
for key1, value1 in states.items():   
    cities[value1] = {}
    for key2, value2 in cl_regions['regions'].items():
        if (key1 in key2 or value1 in key2 or value1.lower() in key2):
            cities[value1][key2] = value2


# print city count and json object for each state to stdout
tot_city_cnt = 0
for key3, value3 in states.items():    
    tot_city_cnt += len(cities[value3])
    print(value3 + ' Count: ' + str(len(cities[value3])))
    print(cities[value3])
    print('\n')    
print("Total cities count: " + str(tot_city_cnt))
print("total states count: " + str(len(states)))

#TODO#
# create json file with all us regions, organized by state
with open('.\\outfiles\\regions_from_cl_us_by_state.json', 'w') as f3:
    json.dump(cities, f3)





# how to print a specific value when you have the key
#print("Value for key 'western maryland': " + str(data['regions']['western maryland']))
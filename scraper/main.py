import time
import os
import requests
import pandas as pd
from multiprocessing.pool import ThreadPool

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


def fanfiction_scrape():
    # Can't get past the cloudflare checkbox atm
    driver = webdriver.Chrome()
    driver.get("https://www.fanfiction.net/book/Lord-of-the-Rings'")
    soup = BeautifulSoup(driver.page_source, 'lxml')
    my_anchors = soup.find_all("a",class_="stitle")
    for anchor in my_anchors[:2]:
        anchor.clear()
        print(anchor)
        time.sleep(3)
        all_iframes = driver.find_elements_by_tag_name("iframe")


        # xpath("//a[@href='/docs/configuration']")).
        print("//a[@href="+anchor['href']+"]")
        username = driver.find_element(By.XPATH, '//a[@href="'+anchor['href']+'"]')
        username.click()
        # driver.get("https://www.fanfiction.net" + anchor['href'])
        # new_soup = BeautifulSoup(driver.page_source, 'lxml')
        # my_divs = soup.find_all("div",class_="storytext")
    driver.close()

# fanfiction_scrape()


def wattapad2():
    print("Starting Wattapad")

    df = pd.read_csv("/Users/sarahcarr/Projects/data_science/lotr_data_pipe/data/lotr.csv")
    print(len(df))
 
    # with ThreadPool() as pool:
    #     for result in pool.map(wattapad_subpage, df.iterrows()):
    #         print(result)
    #     # close the thread pool
    #     pool.close()
    #     # wait for all tasks to complete
    #     pool.join()

       
            
    print("End Wattapad")


def wattapad_subpage(row):
    href = row[1]["on-story-preview href"]
    headers = {
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'en-US,en;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    }
    print(href)
    ps = []
    re = requests.get(href, headers=headers)
    soup = BeautifulSoup(re.text, 'lxml')
    a = soup.find("a", class_="read-btn")

    req = requests.get("https://www.wattpad.com" + a['href'] + href[href.find('-'):] , headers=headers)
    subpage = True
    ind = 1
    while subpage:
        ind += 1
        soup3 = BeautifulSoup(req.text, 'lxml')
        ps.extend(soup3.find_all("p"))
        advance_button = soup3.find("a", class_="btn__Qzch5")
        if not advance_button:
            subpage = False
            continue
        else:
            req = requests.get(advance_button['href'], headers=headers)
    f = open("/Users/sarahcarr/Projects/data_science/lotr_data_pipe/data/lotr/"  +href[40:50]+"-"+str(ind)+ "-scrape.txt", "w")
    f.write(str(ps))
    f.close()




def wattapad():
    headers = {
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'en-US,en;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    }
    r = requests.get("https://www.wattpad.com/stories/lotr", headers=headers)
    # r = requests.get("https://www.wattpad.com/991355215-cat-of-the-fellowship-legolas-x-oc-boromir-x", headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    my_anchors = soup.find_all("a",class_="on-story-preview")
    print(len(my_anchors))
    for anchor in my_anchors[:1]:
        ps = []
        re = requests.get("https://www.wattpad.com" + anchor['href'], headers=headers)
        soup2 = BeautifulSoup(re.text, 'lxml')
        a = soup2.find("a", class_="read-btn")
        req = requests.get("https://www.wattpad.com" + a['href'] +anchor['href'][16:] , headers=headers)
        subpage = True
        while subpage:
            soup3 = BeautifulSoup(req.text, 'lxml')
            ps.extend(soup3.find_all("p"))
            advance_button = soup3.find("a", class_="btn__Qzch5")
            if not advance_button:
                subpage = False
                continue
            else:
                req = requests.get(advance_button['href'], headers=headers)

        # print(ps)
        f = open("/Users/sarahcarr/Projects/data_science/lotr_data_pipe/data/" + anchor['href'][6:]+".txt", "w")
        f.write(str(ps))
        f.close()




  
    




wattapad2()
import requests
import pandas as pd
import os
import json
from multiprocessing.pool import ThreadPool

from bs4 import BeautifulSoup
f = open('../config.json')
config = json.load(f)

columns = ["on-story-preview href","fixed-ratio src","story-rank","title","username","username href","read-count","vote-count","part-count","description","tag-item","tag-item href","tag-item 2","tag-item href 2","tag-item 3","tag-item href 3","num-not-shown","label"]

def wattapad2():
    print("Starting Wattapad")

    df = pd.read_csv(config['file'] + "/lotr.csv", names=columns)
 
    with ThreadPool(processes=3) as pool:
        for result in pool.map(wattapad_subpage, df.iterrows()):
            print(result)
        pool.close()
        pool.join()      
    print("End Wattapad")


def wattapad_subpage(row):
    href = row[1]["on-story-preview href"]
    if os.path.isfile(config['file'] + "/lotrs/"  +href[30:href.find('-')]+ "-scrape.json"):
        print("file exists " +href[30:href.find('-')])
        return
    headers = {
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'en-US,en;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    }
    ps = []
    save_ps = []
    re = requests.get(href, headers=headers)
    soup = BeautifulSoup(re.text, 'lxml')
    a = soup.find("a", class_="read-btn")
    req = requests.get("https://www.wattpad.com" + a['href'] + href[href.find('-'):] , headers=headers)
    subpage = True
    ind = 1
    while subpage:
        ind += 1
        soup3 = BeautifulSoup(req.text, 'lxml')
        ps.extend(soup3.find_all("p", class_=""))
        advance_button = soup3.find("a", class_="btn__Qzch5")
        if not advance_button:
            subpage = False
            continue
        else:
            req = requests.get(advance_button['href'], headers=headers)

    for p in ps:
        save_ps.append(p.getText())
    row[1]['text'] = ' '.join(save_ps)
    df = pd.Series(row[1])
    df.to_json(config['file'] + "/lotrs/"  +href[30:href.find('-')]+ "-scrape.json")

wattapad2()
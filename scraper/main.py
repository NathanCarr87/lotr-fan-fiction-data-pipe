import requests
import pandas as pd
from multiprocessing.pool import ThreadPool

from bs4 import BeautifulSoup


def wattapad2():
    print("Starting Wattapad")

    df = pd.read_csv("/Users/sarahcarr/Projects/data_science/lotr_data_pipe/data/lotr.csv")
    print(len(df))
 
    with ThreadPool() as pool:
        for result in pool.map(wattapad_subpage, df.iterrows()):
            print(result)
        # close the thread pool
        pool.close()
        # wait for all tasks to complete
        pool.join()        
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

wattapad2()
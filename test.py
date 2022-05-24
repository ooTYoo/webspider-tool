# to download the brifing reports from given blackhat url
import os.path

import bs4
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from pywget import wget
import time
import re
import os
import json
from bs4 import BeautifulSoup


bh_url = r'https://www.blackhat.com/us-21/briefings/schedule/'
gDBG = True

def dump_index(url):
    driver = webdriver.Firefox()
    driver.implicitly_wait(15)
    driver.get(url)
    driver.implicitly_wait(5)
    if True:
        html_doc = driver.page_source
        print(len(html_doc))
        log = r'/path/workspace/pyspider/out-bh/index.html'
        log = r'/path/workspace/pyspider/out-bh/index.html'
        with open(log,'wb') as fin:
            fin.write(html_doc.encode('utf-8'))
        print("[+] dump html ok")
    driver.quit()

def item_parse(aitem):
    global gDBG
    domain = r'https://www.blackhat.com/us-21/briefings/schedule/'
    title_element = aitem.find('a',attrs={'class': "sd_link"})
    title = title_element.get_text()
    href = domain + title_element.get('href')

    speaker_element = aitem.find_all('a', attrs={'class': "speaker_link"})
    speakers = []
    for item in speaker_element:
        speakers.append(item.get_text())

    track_element = aitem.find_all('div', class_=re.compile("track_type_iconlist"))
    tracks = []
    for item in track_element:
        tracks.append(item.get("class")[1].split('_')[0])

    if gDBG:
        print(title)
        print(href)
        print(speakers)
        print(tracks)
        print()

    return {'title':title, 'href':href,'speakers':speakers, 'tracks':tracks}


def index_parse():
    log = r'/path/workspace/pyspider/out-bh/index.html'
    log = r'/path/workspace/pyspider/out-bh/index.html'
    soup = BeautifulSoup(open(log),'lxml')
    a = soup.find('div',attrs={'itemprop':"summary"})
    a = soup.find('div', attrs={'class': "data-container"})
    all = soup.find_all('div', attrs={'class': "data-container"})
    print("[+] total %d brifings"%len(all))
    #print(all[2].prettify())
    rslt = []
    for item in all[1:]:
        tmp = item_parse(item)
        rslt.append(tmp)

    files = r'/path/workspace/pyspider/out-bh/bringfs.json'
    files = r'/path/workspace/pyspider/out-bh/bringfs.json'
    with open(files, 'w') as f:
        json.dump(rslt, f)


def get_download_resource(kw="hardware--embedded"):
    files = r'/path/workspace/pyspider/out-bh/bringfs.json'
    files = r'/path/workspace/pyspider/out-bh/bringfs.json'
    driver = webdriver.Firefox()
    driver.implicitly_wait(15)

    with open(files, 'r') as f:
        lyst = json.load(f)

    for a in lyst:
        if kw not in a["tracks"]:
            continue
        #print(a['href'])
        url = pharse_each_link(a['href'],driver)
        print(url)
        if url is None:
            continue
        file_name = wget.filename_from_url(url)
        file_name = os.path.join("/path/workspace/pyspider/out-bh/",file_name)
        file_name = os.path.join("/path/workspace/pyspider/out-bh/",file_name)
        if os.path.exists(file_name):
            continue
        #wget.download(url, out=file_name)
        os.system('wget '+url)
        print("[+] down ok:",file_name)
        #break
    #os.system('mv ./*.pdf /path/workspace/pyspider/out-bh/')
    #os.system('mv ./*.pdf /path/workspace/pyspider/out-bh/')
    driver.quit()

def pharse_each_link(url,driver):
    driver.get(url)
    driver.implicitly_wait(5)
    #a = driver.find_element(By.PARTIAL_LINK_TEXT,"Download").click()
    #a = driver.find_element(By.XPATH,'//*[contains(text(),"Download")]').click()
    html_doc = driver.page_source
    soup = bs4.BeautifulSoup(html_doc,'lxml')
    links = soup.find_all(string=re.compile("Download"))
    for item in links:
        url = item.find_parent().get('href').strip()
        if 'pdf' in url:
            return url

    if False:
        html_doc = driver.page_source
        print(len(html_doc))
        log = r'/path/workspace/pyspider/out-bh/item.html'
        log = r'/path/workspace/pyspider/out-bh/item.html'
        with open(log,'wb') as fin:
            fin.write(html_doc.encode('utf-8'))
        print("[+] dump html ok")

def test1():
    # doesn't work
    url = r'http://i.blackhat.com/USA21/Wednesday-Handouts/us-21-PCIe-Device-Attacks-Beyond-DMA-Exploiting-PCIe-Switches-Messages-And-Errors.pdf'
    file_name = wget.filename_from_url(url)
    file_name = os.path.join("/path/workspace/pyspider/out-bh/", file_name)
    file_name = os.path.join("/path/workspace/pyspider/out-bh/", file_name)
    print(file_name)
    wget.download(url, out=file_name)
    print("[+] down ok:", file_name)

if __name__ == "__main__":
    #dump_index(bh_url)
    #index_parse()
    get_download_resource()

# -*- coding: utf-8 -*-
"""
Created on Thu May  4 20:58:30 2023

@author: wongh
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re

class SeleniumCrawler:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument("--disable-blink-features")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-popup-blocking')
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument('--disable-features=VizDisplayCompositor')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
        chrome_options.add_argument('--lang=en-US,en;q=0.9')
        prefs = {'profile.managed_default_content_settings.images': 2}
        chrome_options.add_experimental_option('prefs', prefs)
        self.driver = webdriver.Chrome(options=chrome_options)

    def crawl_href(self, url):
        prefix_list = url.split("/")[:-1]
        
        self.driver.get(url)
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        hrefs = []
        for a_tag in soup.find_all('a', href=True):
            href = a_tag.get('href')
            if re.match('^http[s]?://', href):
                hrefs.append(href)
            else:
                new_url = '/'.join(prefix_list) + href
                hrefs.append(new_url)
        return hrefs
    
    def crawl_meta(self, url):
        self.driver.get(url)
        page_source = self.driver.page_source
        return page_source
        
    def exit_driver(self):
        self.driver.quit()
        
if __name__ == "__main__":
    crawler = SeleniumCrawler()
    urls = crawler.crawl_href("https://ca.indeed.com/jobs?q=data+scientist&l=&from=searchOnHP&vjk=497de9b404610175")
    for url in urls:
        if "/rc" not in url: continue
        source = crawler.crawl_meta(url)
        break
    crawler.exit_driver()
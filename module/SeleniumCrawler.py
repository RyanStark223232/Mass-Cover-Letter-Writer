# -*- coding: utf-8 -*-
"""
Created on Thu May  4 20:58:30 2023

@author: wongh
"""

import undetected_chromedriver as uc 
from selenium.webdriver.remote.webdriver import By
from bs4 import BeautifulSoup
import re
import trafilatura

class SeleniumCrawler:
    def __init__(self):
        options = uc.ChromeOptions()
        self.driver = uc.Chrome(use_subprocess=True, options=options)
        self.driver.set_window_size(800, 600)

    def crawl_href(self, url, regex_filter = "http"):
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

        filtered_hrefs = [link for link in hrefs if re.search(regex_filter, link)]
        return filtered_hrefs
    
    def crawl_meta(self, url):
        try:
            self.driver.get(url)
            page_source = self.driver.page_source
            html_content = trafilatura.extract(page_source)
        except Exception as e:
            print(f"*** Crawl Failed: {e}")
            page_source = None
            html_content = None
        return page_source, html_content
        
    def exit_driver(self):
        self.driver.quit()

    def get_href_by_css(self, url, css_selector = 'a[aria-label="Next Page"]'):
        try:
            self.driver.get(url)
            element = self.driver.find_element(By.CSS_SELECTOR, css_selector)
            return element.get_attribute('href')
        except:
            print("*** Element Not Found")
            return None

    def get_hrefs_by_css(self, url, css_selector = 'a[aria-label="Next Page"]'):
        try:
            self.driver.get(url)
            elements = self.driver.find_elements(By.CSS_SELECTOR, css_selector)
            return [element.get_attribute('href') for element in elements]
        except:
            print("*** Element Not Found")
            return None

if __name__ == "__main__":
    crawler = SeleniumCrawler()
    base_url = "https://ca.indeed.com/jobs?q=data+scientist&l=&from=searchOnHP&vjk=497de9b404610175"
    job_urls = []
    while base_url is not None:
        urls = crawler.crawl_href(base_url,"/rc")
        job_urls += urls
        base_url = crawler.get_href_by_css(base_url, 'a[aria-label="Next Page"]')
        print(job_urls)

    for url in job_urls:
        _, source = crawler.crawl_meta(url)
        print(source)
    crawler.exit_driver()
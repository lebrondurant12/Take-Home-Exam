# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 21:38:07 2022

@author: howar
"""

import os
import time
import random
from typing import List
from urllib.parse import urlparse, parse_qs

import typer
import joblib
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


URL = "https://rent.591.com.tw/?kind=0&region=3"
browser = webdriver.Chrome(r"C:\Users\howar\OneDrive\桌面\code\cache\chromedriver.exe")


def main(
    output_path: str = "C:/Users/howar/OneDrive/桌面/code/cache/listings.jbl", max_pages: int = 50, quiet: bool = False
):
    try:
        region = parse_qs(urlparse(URL).query)["region"][0]
    except AttributeError as e:
        print("The URL must have a 'region' query argument!")
        raise e
    options = webdriver.ChromeOptions()
    if quiet:
        options.add_argument("headless")
    browser.get(URL)
    browser.maximize_window()
    browser.find_element_by_class_name("statement-confirm").click()
    try:
        browser.find_element_by_css_selector(f'dd[data-id="{region}"]').click()
    except NoSuchElementException:
        pass
    time.sleep(2)
    listings: List[str] = []
    max_pages = int(browser.find_element_by_class_name("pageNext").get_attribute("data-total"))
    for i in range(max_pages):
        print(f"Page {i+1}")
        soup = BeautifulSoup(browser.page_source, "lxml")
        for item in soup.find_all("section", attrs={"class": "vue-list-rent-item"}):
            link = item.find("a")
            listings.append(link.attrs["href"].split("-")[-1].split(".")[0])
        time.sleep(5)
        browser.find_element_by_class_name("pageNext").click()
        time.sleep(random.random() * 5)
        try:
            browser.find_element_by_css_selector("a.last")
            break
        except NoSuchElementException:
            pass
        time.sleep(5)
        try:
            browser.switch_to.alert.accept()
        except Exception:
            pass
    print(len(set(listings)))
    joblib.dump(listings, output_path)
    print(f"Done! Collected {len(listings)} entries.")


if __name__ == "__main__":
    typer.run(main)
    
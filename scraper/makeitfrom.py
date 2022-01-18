"""
Scrape Content from MakeITFrom.com

Tutorials:
https://oxylabs.io/blog/python-web-scraping
"""

import requests
from bs4 import BeautifulSoup
import json
from tqdm import tqdm
import time
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import RequestError
from urllib3.exceptions import NewConnectionError

databasepage = 'https://www.makeitfrom.com'

es = Elasticsearch()
pages = []

with open("makeitfrom_conversion.json", "r") as jfile:
    conversion = json.load(jfile)


def str_to_num(string:str):
    if "." in string:
        return float(string)
    else:
        return int(string)


def scrape_site(url):
    def __scrape_page__(site: str):
        if site in pages:
            return
        pages.append(site)
        connection = False
        response = None
        while not connection:
            time.sleep(1)  # hide activity
            # print(site)
            try:
                response = requests.get(site)
                connection = True
            except NewConnectionError:
                connection = False

        soup = BeautifulSoup(response.content, 'html.parser')
        return soup

    def __extract__(content, site):
        material = dict()
        material["name"] = str(content.find("h1").contents[0])
        material["url"] = str(site)

        res = es.search(index="materials", query={"match": {"url": {"query": material["url"], "operator": "and"}}})
        if res["hits"]["hits"]:
            return

        def __extract_data__(attribute):
            property = dict()
            name = attribute[0].contents[0]
            data = attribute[-1].contents
            value = data[0]
            if len(data) > 1:
                unit = str(data[1].contents[0])
            else:
                unit = ""
            # property["name"] = name
            value = str(value)
            value = value.replace(" ", "")
            if "to" in value:
                values = value.split("to")
            else:
                values = [value, value]
            property["min"] = str_to_num(values[0])
            property["max"] = str_to_num(values[-1])
            property["unit"] = unit
            # print(property)
            if not conversion.get(name):
                print(name)
                conversion[name] = name.lower()
            material[conversion[name]] = property

        for attr in content.find_all(attrs={"class": "mech"}):
            __extract_data__(attr.contents)
        for attr in content.find_all(attrs={"class": "therm"}):
            __extract_data__(attr.contents)
        for attr in content.find_all(attrs={"class": "ele"}):
            __extract_data__(attr.contents)
        for attr in content.find_all(attrs={"class": "other"}):
            __extract_data__(attr.contents)
        for attr in content.find_all(attrs={"class": "common"}):
            __extract_data__(attr.contents)

        if material.get(""):
            material.pop("")

        res = es.index(index="materials", document=material)

    def __scrape__(content, show=False):
        def __scrape__link__(link):
            path = str(link.get('href'))
            site = url+path
            if site in pages:
                return

            if path.startswith('/material-group'):
                html_content = __scrape_page__(site)
                __scrape__(html_content)
            elif path.startswith('/material-properties'):
                html_content = __scrape_page__(site)
                __extract__(html_content, site)
                __scrape__(html_content)

        links = content.find_all('a')
        if show:
            for i in tqdm(range(6, len(links)), desc="Scraping..."):
                link = links[i]
                __scrape__link__(link)
        else:
            for i in range(len(links)):
                link = links[i]
                __scrape__link__(link)

    page_content = __scrape_page__(url + "/")
    __scrape__(page_content, True)


scrape_site(databasepage)


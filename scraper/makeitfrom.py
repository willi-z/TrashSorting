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
    def __extract__(path):
        site = url + path
        pages.append(site)
        response = requests.get(site)
        soup = BeautifulSoup(response.content, 'html.parser')
        material = dict()
        material["name"] = str(soup.find("h1").contents[0])
        material["url"] = str(url + path)

        print("###############")
        # print("extract: " + url + path)
        print("name: " + material["name"])
        print("###############")

        res = es.search(index="materials", query={"match": {"name": material["name"]}})
        if res['hits']['hits']:
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
            property["name"] = name
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
            material[conversion[name]] = property

        for attr in soup.find_all(attrs={"class": "mech"}):
            __extract_data__(attr.contents)
        for attr in soup.find_all(attrs={"class": "therm"}):
            __extract_data__(attr.contents)
        for attr in soup.find_all(attrs={"class": "ele"}):
            __extract_data__(attr.contents)
        for attr in soup.find_all(attrs={"class": "other"}):
            __extract_data__(attr.contents)
        for attr in soup.find_all(attrs={"class": "common"}):
            __extract_data__(attr.contents)

        if material.get(""):
            material.pop("")

        res = es.index(index="materials", document=material)


    def __scrape__(path, show=False):
        time.sleep(0.5)  # hide activity
        site = url + path
        pages.append(site)
        response = requests.get(site)
        soup = BeautifulSoup(response.content, 'html.parser')

        def __scrape__link__(link):
            path = str(link.get('href'))
            if url+path in pages:
                return
            if path.startswith('/material-group'):
                __scrape__(path)
            elif path.startswith('/material-properties'):
                __extract__(path)
                __scrape__(path)

        links = soup.find_all('a')
        if show:
            for i in tqdm(range(len(links)), desc="Scraping..."):
                link = links[i]
                __scrape__link__(link)
        else:
            for i in range(len(links)):
                link = links[i]
                __scrape__link__(link)
    __scrape__("/", True)


scrape_site(databasepage)


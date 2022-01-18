"""
Scrape Content from MakeITFrom.com

Tutorials:
https://matmatch.com
"""
import requests
from bs4 import BeautifulSoup


catagories = ["biological-material", "ceramic", "composite", "glass", "metal", "polymer"]

matmatch_url = "https://matmatch.com"
categories_request = "/advanced-search?categories="


def extract_table_headers(headers):
    for i in range(len(headers)):
        contents = headers[i].contents
        if len(contents) == 1:
            headers[i] = contents[0]
        else:  # Filter out Technological properties as in: https://matmatch.com/materials/nomi0007-epoxy-np130-sheet
            return False
    headers.remove("Comment")
    return True


def extract_materials(materials):
    for material in materials:
        url = matmatch_url + material.get("href")
        print("url: " + str(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        name = soup.find_all("h1")
        name = name[0].contents[0]
        print(name)

        categories = soup.find_all("a", attrs={"class": "styled-link-styles__StyledLinkStyles-sc-l1ctuc-0 dwsZLK"})
        for i in range(len(categories)):
            categories[i] = categories[i].contents[0]
        print(categories)


        tables = soup.find_all("table")
        for table in tables:
            print("#################")
            headers = table.find_all("th")
            if not extract_table_headers(headers):
                continue
            print(headers)
            entities = table.find_all("tr")
            entities = entities[1:]  # delete first, because its header
            for entity in entities:
                tds = entity.find_all("td")
                values = [0] * len(headers)
                for i in range(len(headers)):  # erase "Show Material materials with ...
                    ps = tds[i].find_all("p")
                    content = tds[i].contents
                    if len(ps) >= 1:
                        content = ps[0].contents

                    if len(content) == 1:
                        values[i] = content[0]
                    else:
                        values[i] = None
                print(values)


def scrape_categories():
    start = 1
    for category_counter in range(start, start + 1):
        page = 1
        while True:
            print(page)
            url = matmatch_url + categories_request + catagories[category_counter] + f"&page={page}"
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            # open links which start with /materials/
            links = soup.find_all('a')
            materials = []
            for link in links:
                path = link.get("href")
                if str(path).startswith("/materials/"):
                    materials.append(link)
                    # name = link.contents[0]
                    # print(name)
            if len(materials) == 0:
                break
            extract_materials(materials)
            page += 1


if __name__ == "__main__":
    scrape_categories()



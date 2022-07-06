import requests
from bs4 import BeautifulSoup
from itertools import chain
import re

URL = "https://popvinyls.com/funko-pop-vinyls-series/"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}


def get_links(URL, headers):
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="post-2")
    links = [a["href"] for a in results.find_all("a", href=True)][1:-1]
    return links


def get_brand(link):
    splits = [
        "https://popvinyls.com/",
        "funkopopvinylsseries",
        "funkopopvinylsseries",
        "funko-pop-vinyls-series",
    ]
    drops = ["Pop", "Pops", "Page", "Pages", "Vinyls", "Series"]

    for split in splits:
        link = link.split(split)[-1]
    brand = link.replace("-", " ").replace("/", " ").strip().title()
    return " ".join([word for word in brand.split() if word not in drops]) + " Series"


def clean_pop(pop):
    pop = pop.replace("#", "")
    if not pop[0].isnumeric():
        return None
    return pop


def get_pops(link):
    soup = BeautifulSoup(requests.get(link, headers=headers).content, "html.parser")
    items_html = soup.find_all("div", class_="entry-content clearfix")[0].find_all(
        "figure", class_="gallery-item"
    )
    if len(items_html) == 0:
        pages_links = [
            a["href"]
            for a in soup.find_all("div", class_="entry-content clearfix")[0].find_all(
                "a", href=True
            )
        ]
        pop_lists = [get_pops(page_link) for page_link in pages_links]
        return list(chain(*pop_lists))

    pops = [
        item.find("figcaption").contents[0].strip()
        for item in items_html
        if item.find("figcaption") is not None
    ]

    pops = [pop.replace("#", "") for pop in pops if pop[0].isnumeric() or pop[0] == "#"]
    pops = [
        (int(re.findall(r"\d+", pop)[0]), " ".join(re.findall(r"[a-zA-Z]+", pop)))
        for pop in pops
    ]
    return pops


def get_brand(link):
    splits = [
        "https://popvinyls.com/",
        "funkopopvinylsseries",
        "funkopopvinylsseries",
        "funko-pop-vinyls-series",
    ]
    drops = ["Pop", "Pops", "Page", "Pages", "Vinyls", "Series"]

    for split in splits:
        link = link.split(split)[-1]
    brand = link.replace("-", " ").replace("/", " ").strip().title()
    return " ".join([word for word in brand.split() if word not in drops]) + " Series"


def clean_pop(pop):
    pop = pop.replace("#", "")
    if not pop[0].isnumeric():
        return None
    return pop


def get_pops(link):
    soup = BeautifulSoup(requests.get(link, headers=headers).content, "html.parser")
    items_html = soup.find_all("div", class_="entry-content clearfix")[0].find_all(
        "figure", class_="gallery-item"
    )
    if len(items_html) == 0:
        pages_links = [
            a["href"]
            for a in soup.find_all("div", class_="entry-content clearfix")[0].find_all(
                "a", href=True
            )
        ]
        pop_lists = [get_pops(page_link) for page_link in pages_links]
        return list(chain(*pop_lists))

    pops = [
        item.find("figcaption").contents[0].strip()
        for item in items_html
        if item.find("figcaption") is not None
    ]

    pops = [pop.replace("#", "") for pop in pops if pop[0].isnumeric() or pop[0] == "#"]
    pops = [
        (int(re.findall(r"\d+", pop)[0]), " ".join(re.findall(r"[a-zA-Z]+", pop)))
        for pop in pops
    ]
    return pops


brands = {get_brand(link): link for link in get_links(URL, headers)}
pops = {brand: get_pops(link) for brand, link in brands.items()}

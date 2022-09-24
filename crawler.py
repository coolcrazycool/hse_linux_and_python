import os
import datetime
import requests
from bs4 import BeautifulSoup
from argparse import ArgumentParser

from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
disable_warnings(InsecureRequestWarning)


def get_links(soup):
    links = []
    for link in soup.findAll('a'):
        lnk = link.get('href')
        if lnk is not None and lnk.startswith("http"):
            links.append(lnk)
    return links


def get_content(site):
    page = requests.get(site, verify=False, timeout=2)
    return BeautifulSoup(page.content, "html.parser")


class Crawler:
    def __init__(self, url, max_depth):
        self.url = url
        self.dir_name = f"{datetime.datetime.now().strftime('%Y%m%d_%H-%M-%S')}" \
                        f"_{self.url.replace('http://', '')}_{max_depth}"
        print("Destination is:", self.dir_name)
        self.max_depth = max_depth
        self.urls_dict = {}
        self.counter = 1

        os.mkdir(self.dir_name)

    def save_html(self, content):
        with open(f"{self.dir_name}/{self.counter}.html", "w", encoding='utf-8') as file:
            file.write(str(content.prettify()))

    def save_dict(self):
        with open(f"{self.dir_name}/urls.txt", "w", encoding='utf-8') as file:
            for key, value in self.urls_dict.items():
                file.write(f'{key} {value}\n')

    def get_and_save(self, site):
        soup = get_content(site)
        self.save_html(soup)

        self.urls_dict.update({self.counter: site})
        self.counter += 1

        links = get_links(soup)
        return links

    def recursive_search(self, site, depth=0):
        if depth == self.max_depth:
            try:
                self.get_and_save(site)
            except requests.exceptions.ReadTimeout as e:
                print(str(e))
            except ConnectionError as e:
                print(str(e))
            except requests.exceptions.ConnectionError as e:
                print(str(e))
        else:
            try:
                links = self.get_and_save(site)
                for link in list(set(links) - set(self.urls_dict.values())):
                    self.recursive_search(link, depth + 1)
            except requests.exceptions.ReadTimeout as e:
                print(str(e))
            except ConnectionError as e:
                print(str(e))
            except requests.exceptions.ConnectionError as e:
                print(str(e))

    def search(self):
        self.recursive_search(self.url)
        self.save_dict()


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-s", "--site", dest="site",
                        help="URL address startswith http for crawling", type=str)
    parser.add_argument("-d", "--depth", dest="depth",
                        help="crawling depth", default=1, type=int)

    args = parser.parse_args()
    if args.site is None:
        raise ValueError("You don`t pass the url address!")
    elif not args.site.startswith("http"):
        raise ValueError("URL should be starts with http!")
    elif requests.get(args.site, verify=False).status_code != 200:
        raise ValueError("url is not valid or not working!")
    else:
        crawler = Crawler(args.site, args.depth)
        crawler.search()

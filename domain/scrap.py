# pip3 install requests bs4 colorama
from time import sleep

import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import colorama

# init the colorama module
colorama.init()
GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET
YELLOW = colorama.Fore.YELLOW
FILE_TYPES = (".csv", ".mp4", ".css", ".js", ".png", ".gif", ".tiff", ".3gpp", ".flv",
              ".m4a", ".bat", ".exe")

def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    if parsed.path.lower().endswith(FILE_TYPES):
        return False
    return bool(parsed.netloc) and bool(parsed.scheme)


class DomainUrlScrapper(object):

    def __init__(self, domain=None):
        self.domain = domain
        self.visited_url = []
        self.internal_urls = set()
        self.external_urls = set()

    def scrap(self):
        self.craw_sitemap_xml()
        return self.crawl(self.domain)

    def crawl(self, url):
        links = self.get_all_website_links(url)
        self.visited_url.append(url)
        for link in links:
            if link not in self.visited_url:
                max_retry = 5
                while max_retry:
                    try:
                        self.crawl(link)
                        max_retry = 0
                    except Exception as e:
                        sleep(max_retry)
                        print(str(e))
                        max_retry -= 1
        return self.visited_url

    def craw_sitemap_xml(self):
        urls = set()
        max_retry = 5
        while max_retry:
            try:
                soup = BeautifulSoup(requests.get(self.domain + "/sitemap.xml", verify=False).content, "lxml")
                for url in soup.find_all('url'):
                    urls.add(url.loc.text)
                max_retry = 0
            except Exception as e:
                print(str(e))
                max_retry -= 1

        for link in urls:
            if link not in self.visited_url:
                max_retry = 5
                while max_retry:
                    try:
                        self.crawl(link)
                        max_retry = 0
                    except Exception as e:
                        sleep(max_retry)
                        print(str(e))
                        max_retry -= 1

    def get_all_website_links(self, url):
        """
            Returns all URLs that is found on `url` in which it belongs to the same website
        """
        # all URLs of `url`
        urls = set()
        # domain name of the URL without the protocol
        domain_name = urlparse(url).netloc
        soup = BeautifulSoup(requests.get(url, verify=False).content, "html.parser")
        # print(soup)
        for a_tag in soup.findAll("a"):
            href = a_tag.attrs.get("href")
            if href == "" or href is None:
                # href empty tag
                continue

            href = urljoin(url, href)

            parsed_href = urlparse(href)
            # remove URL GET parameters, URL fragments, etc.
            href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path

            if not is_valid(href):
                # not a valid URL
                continue
            if href in self.internal_urls:
                # already in the set
                continue
            if domain_name not in href:
                # external link
                if href not in self.external_urls:
                    print(f"{GRAY}[!] External link: {href}{RESET}")
                    self.external_urls.add(href)
                continue
            print(f"{GREEN}[*] Internal link: {href}{RESET}")
            urls.add(href)
            self.internal_urls.add(href)
        return urls

#
# if __name__ == "__main__":
#     scrapper = DomainUrlScrapper("https://acquaintsoft.com")
#     l1 = scrapper.scrap()

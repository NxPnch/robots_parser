#! /bin/python3

import urllib
from threading import Thread
import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests


class RobotsParser:

    def __init__(self, url):
        self.url = url
        self.robots_url = f'{url}/robots.txt'

    def check_if_site_is_working(self):
        """This checks if page requests retrieves a 200 response"""

        robots = self.robots_url
        response = requests.get(robots, headers={'User-Agent': 'Mozilla'})
        if response.status_code == 200:
            return True

    def get_robots(self):
        """Appends /robots.txt to the URL and get its content"""

        robots_page = self.robots_url

        if self.check_if_site_is_working():
            response = urllib.request.urlopen(urllib.request.Request(robots_page, headers={'User-Agent': 'Mozilla'}))
            soup = BeautifulSoup(response, 'html.parser', from_encoding=response.info().get_param('charset'))
            return soup.text

    def get_sitemaps(self):
        """Returns the list of sitemap URLs found"""
        robots_file = self.get_robots()
        sitemaps = []

        lines = robots_file.splitlines()

        for line in lines:
            if line.startswith('Sitemap: '):
                sitemaps.append(line.split(':', maxsplit=1)[1].split(' ')[1])

        return '\n'.join(sitemaps)

    def robots_df(self):
        """Parses robots.txt file contents into a pandas dataframe"""
        data = []
        pd.set_option('display.max_rows', None)
        lines = str(self.get_robots()).splitlines()
        for line in lines:
            if line.strip():
                if not line.startswith("#"):
                    split = line.split(":", maxsplit=1)
                    data.append([split[0].strip(), split[1].strip()])

        robots_df = pd.DataFrame(data, columns=['directive', 'parameter'])
        return robots_df

    def parse_requests(self):
        for x in self.robots_df()["parameter"]:
            if x.startswith("/"):
                response = requests.get(f'{self.url}{x}', headers={'User-Agent': 'Mozilla'})
                if response.status_code == 200:
                    print(f'{self.url}{x} -- Returns {response.status_code}')
                else:
                    print(f'{self.url}{x} -- Returns {response.status_code}')


if __name__ == "__main__":
    url = input("Please give me the target URL (Ex: http://target-site.com): \n").strip()
    if url.endswith("/"):
        url = url.strip('/')

    print("VRrrrrrrrrrrrruuuuuuuuuuummmmmmmm.......................\nprrrrpppaaapapa\nrprrsshhhhhh...")
    t1 = Thread(RobotsParser(url).parse_requests())
    t2 = Thread(RobotsParser(url).parse_requests())
    t3 = Thread(RobotsParser(url).parse_requests())
    t4 = Thread(RobotsParser(url).parse_requests())
    t5 = Thread(RobotsParser(url).parse_requests())
    t6 = Thread(RobotsParser(url).parse_requests())

    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()

    print("\n"
          "    Aaaaaaaaaaaaaaaand here are the sitemaps if there's any: \n\n"
          "    ")
    print(RobotsParser(url).get_sitemaps())

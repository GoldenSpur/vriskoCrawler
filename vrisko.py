# !/bin/python3
# -*- coding: UTF-8 -*-

from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import tempfile
import urllib.parse
import os
import codecs


os.system('color e0')
os.system('chcp 28597')
os.system('set PYTHONIOENCODING=utf-8')
os.system('cls')
download_folder = tempfile.gettempdir()


class CrawlVrisko:
    url = None
    page = None
    entries = None

    def __init__(self, url):
        self.url = url

    def open_page(self):
        try:
            self.page = urlopen(self.url).read()
        except:
            return False
        return self.page

    def get_data(self):
        soup = BeautifulSoup(self.page, "html.parser")
        entries = soup.find_all("div", "FreeListingItemBox")
        entries_adv = soup.find_all("div", "AdvItemBox")
        with codecs.open(download_folder + "/" + filename + ".csv", 'a', 'utf-8') as file:
            """"
            This loop collects the free entries
            """""
            for i in entries:
                try:
                    name = i.h2.a.span
                    name = getattr(name, "text")
                except:
                    name = "n/a"
                try:
                    tel = i.find(attrs={"itemprop": "telephone"})
                    tel = getattr(tel, "text")
                except:
                    tel = "n/a"
                try:
                    email = i.find('meta', itemprop="email")["content"]
                except:
                    email = "n/a"
                try:
                    address = i.find("div", "FreeListingAddress")
                    address = getattr(address, "text")
                    address = address.lstrip().strip()
                    address = re.sub(",", "", address)
                except:
                    address = "n/a"
                try:
                    web = i.find("a", "AdvSiteWebSite")["href"]
                except:
                    web = "n/a"
                print(name+","+tel+","+email+","+address+","+web)
                file.write(name+","+tel+","+email+","+address+","+web+"\n")

            """"
            This loop collects the promoted entries
            """""
            for j in entries_adv:
                try:
                    name = j.h2.a.meta["content"]
                except:
                    name = "n/a"
                try:
                    tel = j.find(attrs={"itemprop": "telephone"})
                    tel = getattr(tel, "text")
                except:
                    tel = "n/a"
                try:
                    email = j.find('meta', itemprop="email")["content"]
                except:
                    email = "n/a"
                try:
                    address = j.find("div", "AdvAddress")
                    address = getattr(address, "text")
                    address = address.lstrip().strip()
                    address = re.sub(",", "", address)
                except:
                    address = "n/a"
                try:
                    web = j.find("a", "AdvSiteWebSite")["href"]
                except:
                    web = "n/a"
                print(name+","+tel+","+email+","+address+","+web)
                file.write(name+","+tel+","+email+","+address+","+web+"\n")
        file.close()


if __name__.endswith('__main__'):

    term = True
    while term is True:
        vrisko_link = input("\nPaste here the url of the category you want to crawl \n"
                            "(e.g https://www.vrisko.gr/dir/ekklisies-mones/athina) [Enter to exit]: ").strip()
        os.system('cls')
        print("Data will be saved in this directory: {}\n".format(download_folder))
        filename = vrisko_link.strip("/").split("/")
        try:
            filename_1 = urllib.parse.unquote(filename[-1])
            filename_2 = urllib.parse.unquote(filename[-2])
            filename = filename_1 + "-" + filename_2
        except:
            filename = "new_data"
            print("Check the url you have entered!")
        print("\n")
        with open(download_folder + "/" + filename + ".csv", 'ab') as file:
            file.write(codecs.BOM_UTF8)
        for k in range(0, 11):
            k = str(k)
            vr = CrawlVrisko(vrisko_link + "/?page=" + k)
            if vr.open_page():
                vr.get_data()
                del vr
        if vrisko_link == "":
            term = False

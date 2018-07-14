#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.request, urllib.error
from html.parser import HTMLParser
import re
import os
import zipfile
from tqdm import tqdm
import concurrent.futures

base_url = "https://bulkdata.uspto.gov/data/trademark/application/images/"
year = "2017"
url = os.path.join(base_url, year)
f_list = []
datadir = "/work/data/"
savedir = os.path.join(datadir, "images")


class TrademarkPageParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.fname = ""
        self.fname_list = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            attrs = dict(attrs)
            if 'href' in attrs:
                self.fname = attrs['href']

    def handle_endtag(self, tag):
        if self.fname and re.match('^hrs', self.fname):
            self.fname_list.append(self.fname)
            self.fname = ""

def collect_links(url, f_list):
    response = urllib.request.urlopen(url)

    parser = TrademarkPageParser()
    parser.feed( str(response.read()) )

    f_list.append(parser.fname_list)

    parser.close()
    response.close()

    # Flatten the list
    f_list = [item for sublist in f_list for item in sublist]

    return f_list

def create_link(base_url, year, fname):
    return( os.path.join(base_url, year, fname) )

def download_file(link, savedir):
    fname = os.path.basename(link)
    savefpath = os.path.join(savedir, fname)
    urllib.request.urlretrieve(link, savefpath)
    return savefpath

def unzipfile(fpath, savedir):
    with zipfile.ZipFile(fpath,"r") as zip_ref:
        zip_ref.extractall(savedir)
    os.remove(fpath)
    return

def process_one_file(elem):
    zip_link = create_link(base_url, year, elem)
    try:
        fpath = download_file(zip_link, datadir)
        unzipfile(fpath, savedir)
    except:
        print("Failed to download {}".format(fpath))
        pass

def main():
    print("Start downloading.")
    os.makedirs(savedir, exist_ok=True)
    zip_list = collect_links(url, f_list)

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(process_one_file, elem): elem for elem in zip_list}
        for future in tqdm(concurrent.futures.as_completed(futures)):
            future.result()
    print("Finished downloading.")


if __name__ == '__main__':
    main()

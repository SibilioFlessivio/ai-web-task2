from whoosh.index import create_in
from whoosh.fields import *

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

schema = Schema(title_ix=TEXT(stored=True), content_ix=TEXT(stored=True), url_ix=TEXT(stored=True))

ix = create_in("indexdir", schema)
writer = ix.writer()

prefix = 'https://vm009.rz.uos.de/crawl/'
start_url = prefix+'index.html'
agenda = [start_url]
visited_recently = []
headers_v = []


while agenda:
    url = agenda.pop()
    if url not in visited_recently:
        visited_recently.append(url)
        r = requests.get(url)

        if r.status_code == 200:
            try:
                soup = BeautifulSoup(r.content, 'html.parser')

                content = soup.get_text()
                writer.add_document(title_ix = soup.title.get_text(strip=True) if soup.title else "No Title", content_ix=soup.get_text(), url_ix=url)
                
                for link in soup.find_all('a'):
                    
                    href = link.get('href')
                    # if the href is a relative link, we need to join it with the base url. If the href is an absolut link the function urljoin will return the href as it is.
                    full_url = urljoin(url, href)

                    # we dont want to scrape other weppages than the ones that start with the prefix
                    if full_url.startswith(prefix):
                            agenda.append(full_url)
            except:
                print(f"Error processing {url}")
writer.commit()

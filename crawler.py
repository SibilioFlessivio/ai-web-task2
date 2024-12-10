import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


prefix = 'https://vm009.rz.uos.de/crawl/'
start_url = prefix+'index.html'
agenda = [start_url]
visited_recently = []
index = {}

while agenda:
    url = agenda.pop()
    if url not in visited_recently:
        visited_recently.append(url)
        r = requests.get(url)

        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')

            for link in soup.find_all('a'):
                
                href = link.get('href')
                # if the href is a relative link, we need to join it with the base url. If the href is an absolut link the function urljoin will return the href as it is.
                full_url = urljoin(url, href)

                #in task 2 we dont want to scrape other weppages than the ones that start with the prefix
                if full_url.startswith(prefix):
                        agenda.append(full_url)

print(visited_recently)
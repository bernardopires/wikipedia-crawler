import requests
import Queue

from urlparse import urljoin, urlparse, urldefrag
from BeautifulSoup import BeautifulSoup


def main():
    urls_to_parse = Queue.Queue()
    parsed_urls = []
    urls_to_parse.put('http://en.wikipedia.org/wiki/Main_Page')

    while not urls_to_parse.empty():
        url_to_fetch = urls_to_parse.get()
        if url_to_fetch in parsed_urls:
            continue

        links = find_links(fetch_page(url_to_fetch))

        for link in links:
            if link not in parsed_urls:
                urls_to_parse.put(link)

        parsed_urls.append(url_to_fetch)
        print 'Parsed %s (New queue size: %i)' % (url_to_fetch, urls_to_parse.qsize())


def fetch_page(url):
    # todo check response code and stuff
    return requests.get(url)


def find_links(response):
    soup = BeautifulSoup(response.text)
    return filter(filter_link, [build_link(a['href'], response.url) for a in soup.findAll('a', href=True)])


def filter_link(link):
    # todo: ignore edit, revisions, etc
    excluded_file_types = ('.jpg', '.jpeg', '.png', '.svg', '.gif', '.bmp', '.tiff', '.pdf', '.js', '.css')
    return not link.startswith('#') and urlparse(link).hostname == 'en.wikipedia.org' \
        and not link.endswith(excluded_file_types)


def build_link(link, parent):
    # urljoin is so magical that even if link is an absolute URL it will just use that
    return urldefrag(urljoin(parent, link))[0]


if __name__ == "__main__":
    main()

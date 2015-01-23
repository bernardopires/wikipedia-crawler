import redis
import requests

from bs4 import BeautifulSoup
from crawler.main import app, redis_pool
from urlparse import urljoin, urlparse, urldefrag
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@app.task
def fetch_url(url):
    # todo check response code and stuff
    parse_response.delay(requests.get(url))


@app.task
def parse_response(response):
    links = find_links(response)
    r = redis.Redis(connection_pool=redis_pool)

    for link in links:
        if r.sadd(urlparse(link).hostname, link):
            fetch_url.delay(link)


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

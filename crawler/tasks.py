import codecs
import redis
import requests
import os
import time

from bs4 import BeautifulSoup
from crawler.main import app, redis_pool
from urlparse import urljoin, urlparse, urldefrag
from celery.utils.log import get_task_logger
from requests.exceptions import ConnectionError, RequestException

logger = get_task_logger(__name__)


@app.task
def fetch_url(url):
    # todo check response code and stuff
    try:
        response = requests.get(url)
        parse_response.delay(requests.get(url))
    except ConnectionError:
        logger.warning("Sleeping for 5 seconds...")
        time.sleep(5)
        fetch_url.delay(url)
    except RequestException:  # all other exceptions
        logger.warning("Ignoring url: %s" % url)
        pass


@app.task
def parse_response(response):
    links = find_links(response)
    r = redis.Redis(connection_pool=redis_pool)

    for link in links:
        if r.sadd(urlparse(link).hostname, link):
            fetch_url.delay(link)

    save_response(response)


def find_links(response):
    soup = BeautifulSoup(response.text)
    return filter(filter_link, [build_link(a['href'], response.url) for a in soup.findAll('a', href=True)])


def filter_link(link):
    # todo: ignore edit, revisions, etc
    parsed_url = urlparse(link)
    return not link.startswith('#') and parsed_url.hostname == 'en.wikipedia.org' \
            and "File:" not in parsed_url.path


def build_link(link, parent):
    # urljoin is so magical that even if link is an absolute URL it will just use that
    return urldefrag(urljoin(parent, link))[0]


def save_response(response):
    parsed_url = urlparse(response.url)
    filename = "%s" % parsed_url.hostname + parsed_url.path
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    with codecs.open(filename, "w", "utf-8-sig") as f:
        f.write(response.text)

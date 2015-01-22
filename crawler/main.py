from celery import Celery

app = Celery('crawler',
             broker='amqp://',
             backend='amqp://',
             include=['crawler.tasks'])

app.conf.CELERY_ROUTES = {
    'crawler.tasks.fetch_url': {'queue': 'fetch_queue'},
    'crawler.tasks.parse_response': {'queue': 'parse_queue'},
}


if __name__ == "__main__":
    app.start()

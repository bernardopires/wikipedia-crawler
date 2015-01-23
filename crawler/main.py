import redis
from celery import Celery

app = Celery('crawler',
             broker='amqp://',
             include=['crawler.tasks'])

app.conf.update(
    CELERY_ROUTES =  {
        'crawler.tasks.fetch_url': {'queue': 'fetch_queue'},
        'crawler.tasks.parse_response': {'queue': 'parse_queue'},
    },
    CELERY_ACCEPT_CONTENT = ['json'],
    CELERY_TASK_SERIALIZER = 'json',
    CELERY_MESSAGE_COMPRESSION = 'zlib',
)

redis_pool = redis.ConnectionPool(host='localhost', port=6379, db=0)


if __name__ == "__main__":
    app.start()

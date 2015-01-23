A simple wikipedia crawler in python.

Running:
celery worker -A crawler.tasks --loglevel=info -Q fetch_queue -n 'fetcher'
celery worker -A crawler.tasks --loglevel=info -Q parse_queue -n 'parser'

For monitoring:
celery -A crawler.tasks flower --broker=amqp://guest:guest@localhost:5672// --broker_api=http://guest:guest@localhost:15672/api/

https://www.rabbitmq.com/management.html
rabbitmq-plugins enable rabbitmq_management

Flower: http://localhost:5555/
RabbitMQ: http://localhost:15672/

Why only wikipedia => pretty much guaranteed sane HTML

A simple wikipedia crawler in python.

Running:
celery worker -A crawler.tasks --loglevel=info -Q fetch_queue -n 'fetcher'
celery worker -A crawler.tasks --loglevel=info -Q parse_queue -n 'parser'

For monitoring:
celery -A crawler.tasks flower
http://localhost:5555/

Why only wikipedia => pretty much guaranteed sane HTML

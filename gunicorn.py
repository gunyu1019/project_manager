from multiprocessing import cpu_count

bind = "127.0.0.1:8000"

workers = 10
worker_class = "gevent"

wsgi_app = "app:create_app()"

accesslog = "-"
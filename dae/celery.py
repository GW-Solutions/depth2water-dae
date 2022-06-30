from celery import Celery


app = Celery('dae', broker='amqp://guest@localhost//')
app.autodiscover_tasks(['dae', 'dae.example'])


if __name__ == '__main__':
    app.start()

from celery import Celery
app = Celery('mock', broker='redis://redis:6379/0')
@app.task
def heartbeat():
    return 'ok'

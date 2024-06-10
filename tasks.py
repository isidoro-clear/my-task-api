from celery import Celery

app = Celery('tasks', broker='redis://127.0.0.1:6379/0')

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

@app.task
def add(x, y):
  return x + y
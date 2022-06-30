# depth2water-dae

## Setup
```
# Install Celery and Rabbitmq message queue 
$ pip install celery
$ sudo apt-get install rabbitmq-server


# Clone the repo and start the task queue
$ git clone git@github.com:GW-Solutions/depth2water-dae.git
$ cd depth2water-dae
$ celery -A dae worker -B --loglevel=INFO
```
Assuming everything went smoothly, your terminal should now be displaying the Celery logs and printing "Hello World!" every 10 seconds.


## Adding a task
In your terminal:
```python
# Create a feature branch (from repo base dir `depth2water-dae`)
$ git checkout -b my-new-task

# Create required project directory/file structure
$ mkdir dae/<my_task_directory_name>
$ touch dae/<my_task_directory_name>/__init__.py && touch dae/<my_task_directory_name>/tasks.py
```
In your editor:
```python
# Configure the Celery task auto discovery
# In celery.py, add the name of your package to the `autodiscover_tasks` method
app.autodiscover_tasks(['dae', 'dae.example', 'dae.my_task_directory_name'])


# Create task in dae/<my_task_directory_name>/tasks.py
# (task code is arbitrary, in your case it will be depth2water-client code)
from dae.celery import app
from celery.schedules import crontab


# Task that simply prints its arg. @app.task is the key here.
@app.task
def test(arg):
    print(arg)
    
    
# Register the task with the scheduler
@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('Hello World!') every 10 seconds.
    sender.add_periodic_task(10.0, test.s('Hello World!'), name='add every 10')

    # Calls test every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        test.s('Happy Mondays!'),
    )
```
After adding your task, simply restart the task queue and you should see your task run right on schedule:
```
$ ctrl+c
$ celery -A dae worker -B --loglevel=INFO
```
Open a PR on Github. Dave will approve, merge, and deploy to prod.
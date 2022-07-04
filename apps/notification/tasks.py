from celery import shared_task

from prosit.celery import app



@app.task()
def run_task():

	for i in range(20):
		print(i)
	return "Done"


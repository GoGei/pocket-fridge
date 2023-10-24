from celery_run import app
from core.Finances.stripe import utils


@app.task(ignore_result=True)
def load_invoices_task():
    utils.load_invoices(raise_errors=False)


@app.task(ignore_result=True)
def load_payments_task():
    utils.load_payments(raise_errors=False)

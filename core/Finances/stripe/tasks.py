from celery_run import app
from . import utils


@app.task(ignore_result=True)
def load_invoices():
    utils.load_invoices(raise_errors=False)


@app.task(ignore_result=True)
def load_payments():
    utils.load_payments(raise_errors=False)

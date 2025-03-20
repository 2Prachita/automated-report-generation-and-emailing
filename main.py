from datetime import datetime, timedelta
from prefect.flows import flow 
from prefect.tasks import task
from config import DATE, FORMAT
from reportemail import daily_sale_report_email
from reports import generate_daily_sales_report
from prefect.logging import get_logger

log = get_logger()

@task
def generate_report(date: datetime):
    generated= generate_daily_sales_report(date)
    if generated:
        log.info("Report generated sucessfully!")
    else:
        log.info("Report not generated")

@task
def email_report(date: datetime):
    sent = daily_sale_report_email(date)
    if sent :
        log.info("Email sent")
    else :
        log.info("Email sending failed")

@flow
def daily_sales_report():
    
    date = datetime.now() - timedelta(days=1)
    tDate = datetime.strptime(DATE, "%Y-%m-%d")
    generate_report(tDate)
    email_report(tDate)

if __name__ == "__main__":
    daily_sales_report()
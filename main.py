from datetime import datetime, timedelta
from prefect.flows import flow 
from prefect.tasks import task
from config import DATE, FORMAT
import logging
from reportemail import daily_sale_report_email
from reports import generate_daily_sales_report

logging.basicConfig(level=logging.INFO, format=FORMAT)

@task
def generate_report(date: datetime):
    generated= generate_daily_sales_report(date)
    if generated:
        print("Report generated sucessfully!")
    else:
        print("Report not generated")

@task
def email_report(date: datetime):
    sent = daily_sale_report_email(date)
    print(sent)

@flow
def daily_sales_report():
    
    date = datetime.now() - timedelta(days=1)
    tDate = datetime.strptime(DATE, "%Y-%m-%d")
    generate_report(tDate)
    email_report(tDate)

if __name__ == "__main__":
    daily_sales_report()
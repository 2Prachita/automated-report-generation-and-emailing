from datetime import datetime, timedelta
from prefect import flow
from prefect.schedules import Interval


if __name__ == "__main__":
    flow.from_source(
        source="https://github.com/2Prachita/automated-report-generation-and-emailing.git",
        entrypoint="main.py:daily_sales_report"
    ).deploy(
        name="daily-auto-report-generation",
        work_pool_name="my-work-pool",
        cron="0 17 * * *",
    )
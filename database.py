from datetime import datetime
import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from config import DB_NAME, DB_USER, DB_HOST, DB_PASS
from prefect.logging import get_logger

log = get_logger()

def insert_data(data : pd.DataFrame) -> bool:
    try: 
        with psycopg2.connect(
            database=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST
        ) as connection: 
            with connection.cursor() as cursor:
                query = """INSERT INTO SALES(date, time, order_number, article, quantity, unit_price) 
                        VALUES ( %s, %s, %s, %s, %s, %s)"""
                value = (data["date"],
                        data["time"],
                        data["order_number"],
                        data["article"],
                        data["quantity"],
                        data["unit_price"])
                cursor.execute(query, value)
    except Exception as e:
        log.error(f"Database error: {e}")

def get_data(date : datetime) -> list:

    try:
        with psycopg2.connect(
            database=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST
        ) as connection:
            with connection.cursor() as cursor:
                query = f"""SELECT * FROM SALES WHERE date = '{date:%Y-%m-%d}'"""
                print(query)
                cursor.execute(query)
                return cursor.fetchall()

    except Exception as e:
        log.error(e)

def insert_data_from_csv(data: pd.DataFrame) -> bool:

    try:
        'postgresql://username:password@localhost:5432/your_database'
        db_url = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}'
        engine = create_engine(db_url)
        print(type(data))
        data.to_sql(name="sales", con=engine, if_exists="replace", index=False)
        log.info("Inserted sucessfully!")
        return True
    
    except Exception as e:
        log.error("Insertion failed")
        return False
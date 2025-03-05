from datetime import datetime
import logging
import psycopg2
from config import DB_NAME, DB_USER, DB_HOST, DB_PASS

def insert_data(data : dict) -> bool:
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
        logging.error(f"Database error: {e}")

def get_data(date : datetime) -> list:

    try:
        with psycopg2.connect(
            database=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST
        ) as connection:
            with connection.cursor() as cursor:
                query = f"""SELECT * FROM SALES WHERE date = '{date: %Y-%m-%d}'"""
                cursor.execute(query)
                return cursor.fetchall()

    except Exception as e:
        logging.error(e)
import logging
import pandas as pd
from prefect import flow, task
from concurrent.futures import ThreadPoolExecutor
from config import FORMAT
from database import insert_data

logging.basicConfig(level=logging.INFO, format=FORMAT)


@task(name="Extracting Data")
def extract_from_csv() -> pd.DataFrame:
    sales = pd.read_csv("Bakery sales.csv")
    sales = sales.drop('unwanted', axis=1)
    sales = sales.rename(columns={'ticket_number': 'order_number', 'Quantity': 'quantity'})
    sales["unit_price"] =  sales["unit_price"].str.replace(" €", "", regex=True)
    sales["unit_price"] =  sales["unit_price"].str.replace(",", ".", regex=True)
    sales["unit_price"] = sales["unit_price"].astype(float)
    return sales.to_dict(orient="records")


@task(name="Saving Data")
def save_to_db(data : dict):
    if data is None :
        raise ValueError("Dataframe is empty or None")
    inserted = insert_data(data)
    if inserted:
        logging.info("Data sucessfully inserted in the database")
    else:
        logging.error("Data not inserted. Error occured")


@flow(name="Data Ingestion Pipeline")
def data_ingestion():
    data = extract_from_csv()
    with ThreadPoolExecutor(max_workers=10) as executor:  # Adjust workers as needed
        executor.map(save_to_db, data)


if __name__ == "__main__":
    data_ingestion()
import pandas as pd
from prefect import flow, task
from concurrent.futures import ThreadPoolExecutor
from config import FORMAT
from database import insert_data, insert_data_from_csv
from prefect.logging import get_logger

log = get_logger()

@task(name="Extracting Data")
def extract_from_csv() -> pd.DataFrame:
    sales = pd.read_csv("Bakery sales.csv")
    #sales = sales.drop('unwanted', axis=1)
    sales = sales.rename(columns={'ticket_number': 'order_number', 'Quantity': 'quantity'})
    sales["unit_price"] =  sales["unit_price"].str.replace(" €", "", regex=True)
    sales["unit_price"] =  sales["unit_price"].str.replace(",", ".", regex=True)
    sales["unit_price"] = sales["unit_price"].astype(float)
    log.info("Data Extracted from csv")
    return sales#.to_dict(orient="records")


@task(name="Saving Data")
def save_to_db(data : pd.DataFrame):
    if data is None :
        raise ValueError("Dataframe is empty or None")
    inserted = insert_data_from_csv(data)
    if inserted:
        log.info("Data sucessfully inserted in the database")
    else:
        log.error("Data not inserted. Error occured")


@flow(name="Data Ingestion Pipeline")
def data_ingestion():
    data = extract_from_csv()
    save_to_db(data)
    '''with ThreadPoolExecutor(max_workers=10) as executor:  # Adjust workers as needed
        executor.map(save_to_db, data)'''
    

if __name__ == "__main__":
    data_ingestion()
import logging
import os
from datetime import datetime
from pathlib import Path

from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

logger = logging.getLogger(__name__)


with DAG(dag_id="monolith", start_date=datetime(2022, 1, 1), schedule="0 0 * * *") as dag:

    @task()
    def load_data():
        logger.info("Executing load_data")
        import pandas as pd
        from sqlalchemy import create_engine
        engine = create_engine(
            "postgresql+psycopg2://postgres:password@host.docker.internal:5433/postgres", echo=True
        )
        TABLE_NAME = "credit_cards"
        csv_file_path = '/opt/airflow/data/creditcard_2023.csv'
        with open(csv_file_path, 'r') as file:
            df = pd.read_csv(file)
        df.to_sql(TABLE_NAME,
                  con=engine,
                  index=False,
                  if_exists='replace')

    clean_data_and_create_view = PostgresOperator(
        task_id="clean_data",
        postgres_conn_id="local_db",
        sql='sql/data_cleaning.sql')

    @task()
    def load_model():
        logger.info("Executing load_model")
        import joblib
        import pandas as pd
        import psycopg2
        model = joblib.load("/opt/airflow/data/credit_card_model.pkl")
        logger.info("Connecting to DB")
        connection = psycopg2.connect(database="postgres", user="postgres", password="password", host='host.docker.internal',
                                      port=5433)

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM normalised_data")
                colnames = [desc[0] for desc in cursor.description]
                tuples_list = cursor.fetchall()
        finally:
            connection.close()

        data = pd.DataFrame(tuples_list, columns=colnames)
        data['Fraud'] = model.predict(data)
        logger.info("Saving results as parquet")
        data.to_parquet('/opt/airflow/data/results.parquet')


    load_data() >> clean_data_and_create_view >> load_model()
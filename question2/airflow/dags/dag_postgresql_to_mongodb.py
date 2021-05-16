import datetime as dt
import pandas as pd
import json
import subprocess
from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator


def _install_tools():
    try:
        import psycopg2 
    except:
        subprocess.check_call(['pip' ,'install', 'psycopg2-binary' ])
        import psycopg2

    try:
        from sqlalchemy import create_engine
    except:
        subprocess.check_call(['pip' ,'install', 'sqlalchemy' ])
        from sqlalchemy import create_engine

    try:
        import pandas as pd 
    except:
        subprocess.check_call(['pip' ,'install', 'pandas' ])
        import pandas as pd
    
    try:
        from pymongo import MongoClient
    except:
        subprocess.check_call(['pip', 'install', 'pymongo'])
        from pymongo import MongoClient


 
def postgresql_table_to_json():
    # For some reason, I have to reimport the required packages because airflow does not
    #  recognize the imports done in a previous step (I haven't figured out the cause)
    from sqlalchemy import create_engine
    
    # Changed host="dev-postgres" (docker container name)
    # Requires adding all containers to one docker network so sqlalchemy would connect to the postgres docker container by
    #  docker container name instead of ip address (create_docker_network.sh in parent directory).
    host="dev-postgres"
    database="testDB"
    user="me"
    password="1234"
    port='5432'
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')

    # Reading postgresql table
    df_telco = pd.read_sql("SELECT * FROM telco" , engine)
    df_telco.to_json('/opt/airflow/dags/data/telco.json', orient='records')
    # Close sqlalchemy engine
    engine.dispose()


def json_to_mongodb_collection():
    # For some reason, I have to reimport the required packages because airflow does not
    #  recognize the imports done in a previous step (I haven't figured out the cause)
    from pymongo import MongoClient

    # Changed from mongo:27017 to mongo-db:27017 (docker container name)
    mongo_client = MongoClient('mongo-db:27017', username='root', password='example')
    tamer_db = mongo_client["tamer"]
    telco_collection = tamer_db.telco

    # Reading generated json file
    with open('/opt/airflow/dags/data/telco.json') as file:
        file_data = json.load(file)
    
    # Insert to MongoDB collection
    telco_collection.insert_many(file_data)

    # Close MongoDB connection
    mongo_client.close()
 
 
default_args = {
    'owner': 'Tamer',
    'start_date': dt.datetime(2021, 5, 15),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=1)
}
 
with DAG('dag_postgresql_to_json_to_mongodb', default_args=default_args, schedule_interval=timedelta(minutes=1), catchup=False) as dag:
    install_tools = PythonOperator(task_id="install_tools", python_callable=_install_tools)
    postgresql_to_json = PythonOperator(task_id='postgresql_to_json', python_callable=postgresql_table_to_json)
    json_to_mongodb = PythonOperator(task_id='json_to_mongodb', python_callable=json_to_mongodb_collection)
 
install_tools >> postgresql_to_json >> json_to_mongodb

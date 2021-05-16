### Question 2
Implementing an Airflow pipeline where a csv file that is previously inserted into a PostgreSQL database would be read and converted into a JSON file whereby it would be pushed into a MongoDB database.

The README will cover on how to run the Airflow pipeline. For the detailed implementation please check the 'question2.pptx' powerpoint file.

#### Running the pipeline

1. Open a terminal at the current directory then run ```docker-compose up```
2. Open a terminal at the 'airflow' directory then run ```docker-compose up```
3. After all the docker containers are initialized run ```./create_docker_network.sh``` as the localnet network did not work and I had to create a new docker network and add the running docker containers to it in order for the docker containers to communicate with each other
4. Navigate to localhost:8000 (pgadmin) (user: 1234@admin.com, password: 1234) and Add a new server with name: postgres, Hostname/Address: postgres, Username: me, Password: 1234
5. Navigate to localhost:8888 (jupyterlab) and run all cells in the '1-Insert_csv_file_to_PostgreSQL.ipynb' jupyter notebook to insert the Kaggle telco customer churn csv file into the postgresql database
6. Navigate to localhost:8081 (mongo express) and create a new database with the name 'tamer' with collection 'telco'
7. Navigate to localhost:8080 (airflow) (username and password: airflow) and run the 'dag_postgresql_to_json_to_mongodb' dag
8. If the dag is successful, then there will be a new json file being created at 'airflow/data' and the mongodb collection would be filled with new documents (I used insert_many so there will be duplicate records each run).

Note: If there is a connection issue between the containers; re-running the ```./create_docker_network.sh``` script might fix the issue

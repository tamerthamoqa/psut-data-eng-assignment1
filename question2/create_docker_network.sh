# Create docker network so the docker container would be able to connect with
#  each other by name instead of ip
docker network create network

# Add running docker containers to the network
docker network connect network airflow_airflow-scheduler_1
docker network connect network airflow_airflow-webserver_1
docker network connect network airflow_airflow-worker_1
docker network connect network airflow_airflow-scheduler_1
docker network connect network airflow_flower_1
docker network connect network airflow_postgres_1
docker network connect network airflow_redis_1

docker network connect network dev-postgres
docker network connect network mongo-db

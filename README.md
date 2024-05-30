This project relies on docker and terraform. 
Please run the commands below in the order encountered

To set up terraform run

`cd terraform` (navigate to the terraform directory)

`terraform init`

To initialise the airflow db

`docker compose up airflow-init`

Now all services can be started

`docker-compose up -d`

The user must go into localhost(http://localhost:8080/home) at this stage and add a connection,
add the following (username and password are both airflow):

Conn Id: local_db
Conn type: Postgres
Host: host.docker.internal
Port: 5433

The required input data should now be placed in terraform/data


To run the DAG execute

`docker compose run airflow-worker dags test monolith
`

To run a particular task run

`docker compose run airflow-worker tasks test monolith my_first_dag 2022-02-02
`

To terminate services at any point run

`docker compose down`



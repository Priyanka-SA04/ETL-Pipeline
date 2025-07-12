### Project Overview: Airflow ETL Pipeline with Postgres and API Integration
This project involves creating an ETL (Extract, Transform, Load) pipeline using Apache Airflow. The pipeline extracts data from an external API — NASA's Astronomy Picture of the Day (APOD) API — transforms the data, and loads it into a Postgres database. The entire workflow is orchestrated by Airflow, a platform that allows scheduling, monitoring, and managing workflows.
The project leverages Docker to run Airflow and Postgres as services, ensuring an isolated and reproducible environment. We also utilize Airflow Hooks and the TaskFlow API to handle the ETL process efficiently.

Key Components of the Project:

Airflow for Orchestration:
Airflow is used to define, schedule, and monitor the entire ETL pipeline. It manages task dependencies, ensuring that the process runs sequentially and reliably. The Airflow DAG (Directed Acyclic Graph) defines the workflow, which includes tasks like data extraction, transformation, and loading.
We use the TaskFlow API (@task decorator) to simplify task definitions and improve readability.

Postgres Database:
A PostgreSQL database is used to store the extracted and transformed data. Postgres runs in a Docker container for portability and persistence using Docker volumes. We interact with the database using Airflow’s PostgresHook, which allows executing raw SQL queries directly from Python functions

NASA API (Astronomy Picture of the Day):
The external API used in this project is NASA’s APOD API, which provides astronomy picture metadata including the title, explanation, date, and media type. We use Airflow’s HttpHook to make HTTP GET requests and retrieve the JSON response.


Objectives of the Project:

Extract Data:
The pipeline extracts astronomy-related data from NASA’s APOD API on a scheduled basis (daily, in this case).

Transform Data:
Transformations such as filtering or processing the API response are performed to ensure that the data is in a suitable format before being inserted into the database.

Load Data into Postgres:
The transformed data is loaded into a Postgres database. The data can be used for further analysis, reporting, or visualization.

Architecture and Workflow:
The ETL pipeline is orchestrated in Airflow using a DAG (Directed Acyclic Graph). The pipeline consists of the following stages:
1. Extract (E):
The pipeline extracts astronomy-related data from NASA’s APOD API on a scheduled basis (daily). This is done using the HttpHook to send GET requests and retrieve structured JSON responses.
2. Transform (T):
The extracted JSON data is processed in the transform task using Airflow’s TaskFlow API (with the @task decorator).
This stage involves extracting relevant fields like title, explanation, url, and date and ensuring they are in the correct format for the database.
3. Load (L):
The transformed data is loaded into a Postgres table using PostgresHook.
If the target table doesn’t exist in the Postgres database, it is created automatically as part of the DAG using a create table task.

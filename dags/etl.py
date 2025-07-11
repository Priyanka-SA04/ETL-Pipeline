from airflow import DAG
from airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.http.hooks.http import HttpHook
from airflow.utils.dates import days_ago
##https://api.nasa.gov/planetary/apod?api_key=eXAs7zYVXDWMz77rQLWw340iaazt9Q3ASonmZ99b

with DAG(
    dag_id='nasa_apod_postgres',
    start_date=days_ago(1),
    schedule='@daily',
    catchup=False
    
) as dag:

    @task
    def create_table():
        postgres_hook = PostgresHook(postgres_conn_id="my_postgres_connection")
        create_table_query = """
        CREATE TABLE IF NOT EXISTS apod_data (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255),
            explanation TEXT,
            url TEXT,
            date DATE,
            media_type VARCHAR(50)
        );
        """
        postgres_hook.run(create_table_query)

    @task
    def extract_apod():
        hook = HttpHook(method='GET', http_conn_id='nasa_api')
        response = hook.run(
            endpoint='planetary/apod',
            data=None,
            extra_options={},
            headers={},
            params={"api_key": "{{ conn.nasa_api.extra_dejson.api_key }}"}
        )
        return response.json()

    @task
    def transform_apod_data(response):
        apod_data = {
            'title': response.get('title', ''),
            'explanation': response.get('explanation', ''),
            'url': response.get('url', ''),
            'date': response.get('date', ''),
            'media_type': response.get('media_type', '')
        }
        return apod_data

    @task
    def load_data_to_postgres(apod_data):
        postgres_hook = PostgresHook(postgres_conn_id='my_postgres_connection')
        insert_query = """
        INSERT INTO apod_data (title, explanation, url, date, media_type)
        VALUES (%s, %s, %s, %s, %s);
        """
        postgres_hook.run(insert_query, parameters=(
            apod_data['title'],
            apod_data['explanation'],
            apod_data['url'],
            apod_data['date'],
            apod_data['media_type']
        ))

    # DAG execution chain
    create_table() >> load_data_to_postgres(transform_apod_data(extract_apod()))

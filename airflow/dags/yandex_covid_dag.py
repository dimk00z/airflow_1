import requests
import csv
import os
import json
from pathlib import Path

from airflow.utils.dates import days_ago

from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator

YANDEX_COVID_URL = 'https://yastat.net/s3/milab/2020/covid19-stat/data/data_struct_10.json?v=timestamp'


def get_json_from_yandex():
    response = requests.get(YANDEX_COVID_URL)
    response.raise_for_status()
    return response.json()


def parse_yandex_covid_json():
    covid_json = get_json_from_yandex()
    dates = covid_json['russia_stat_struct']['dates']
    regions = [['date', 'region', 'infected', 'recovered', 'dead']]
    for region_number in covid_json['russia_stat_struct']['data']:
        region = covid_json['russia_stat_struct']['data'][region_number]
        region_name = region['info']['name']
        if region_name == 'Россия':
            continue
        region_statistic = []
        for date_number, date in enumerate(dates):
            infected = region['cases'][date_number]['v']
            recovered = region['cured'][date_number]['v']
            dead = region['deaths'][date_number]['v'] if region['deaths'] else 0
            date_statistic = {date: {
                'infected': infected,
                'recovered': recovered,
                'dead': dead}
            }
            regions.append([
                date, region_name, infected, recovered, dead
            ])
    return regions


def write_csv(file_name='covid.csv', dest_folder=Path.cwd(),**kwargs):
    regions = parse_yandex_covid_json()
    csv_file_name = Path.joinpath(
        dest_folder, file_name)
    with open(csv_file_name, 'w+', encoding='utf-8') as f:
        writer = csv.writer(f)
        for row in regions:
            writer.writerow(row)


args = {
    'owner': 'Airflow',
    'start_date': days_ago(2),
}

dag = DAG(
    dag_id='yandex_covid_python_operator',
    default_args=args,
    schedule_interval='0 12 * * *',
    tags=['yandex, covid']
)


run_this = PythonOperator(
    task_id='get_covid_data',
    provide_context=True,
    python_callable=write_csv,
    # op_kwargs={'dest_folder': '/home/dimk/Python/airflow_course/airflow_1/'},
    dag=dag,
)
# [END howto_operator_python]


# # [START howto_operator_python_kwargs]
# def my_sleeping_function(random_base):
#     """This is a function that will run within the DAG execution"""
#     time.sleep(random_base)


# Generate 5 sleeping tasks, sleeping from 0.0 to 0.4 seconds respectively

# task = PythonOperator(
#         task_id='sleep_for_' + str(i),
#         python_callable=my_sleeping_function,
#         op_kwargs={'random_base': float(i) / 10},
#         dag=dag,
#     )

# run_this >> task
# [END howto_operator_python_kwargs]

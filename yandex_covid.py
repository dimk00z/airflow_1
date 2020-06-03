import requests
import csv
import os
import json
from pathlib import Path

YANDEX_COVID_URL = 'https://yastat.net/s3/milab/2020/covid19-stat/data/data_struct_10.json?v=timestamp'


def get_json_from_yendex():
    response = requests.get(YANDEX_COVID_URL)
    response.raise_for_status()
    return response.json()


def parse_yandex_covid_json(json):
    dates = json['russia_stat_struct']['dates']
    regions = [['date', 'region', 'infected', 'recovered', 'dead']]
    for region_number in json['russia_stat_struct']['data']:
        region = json['russia_stat_struct']['data'][region_number]
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


def write_covid_csv(regions, file_name='covid.csv', dest_folder=Path.cwd()):
    csv_file_name = Path.joinpath(
        dest_folder, file_name)
    with open(csv_file_name, 'w+', encoding='utf-8') as f:
        writer = csv.writer(f)
        for row in regions:
            writer.writerow(row)


def main():
    yandex_covid = get_json_from_yendex()
    write_covid_csv(parse_yandex_covid_json(yandex_covid))


if __name__ == '__main__':
    main()

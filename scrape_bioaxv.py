import requests
import json
from datetime import datetime
import time
import random
from dateutil.relativedelta import relativedelta

def download_json_data(url, output_file):
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        with open(output_file, 'w') as f:
            json.dump(data, f)
        print(f"JSON data saved to {output_file}.")
    else:
        print(f"Error: Unable to download JSON data from {url}. Status code {response.status_code}.")

def generate_urls(start_date, end_date):
    date_format = "%Y-%m-%d"
    current_date = datetime.strptime(start_date, date_format)
    end_date = datetime.strptime(end_date, date_format)

    urls = []
    while current_date < end_date:
        next_month = current_date + relativedelta(months=1)
        url = f"https://api.biorxiv.org/details/biorxiv/{current_date.strftime(date_format)}/{next_month.strftime(date_format)}/100"
        urls.append(url)
        current_date = next_month

    return urls

if __name__ == "__main__":
    start_date = "2021-01-01"
    end_date = "2023-03-01"

    urls = generate_urls(start_date, end_date)

    for index, url in enumerate(urls):
        output_file = f"data/abstracts/json/data_{index + 1}.json"
        delay = random.uniform(1, 5)  # Random delay between 1 and 5 seconds
        time.sleep(delay)
        download_json_data(url, output_file)

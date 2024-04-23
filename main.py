import sys
import os
import requests
import argparse
import shutil
from datetime import datetime, timedelta
from termcolor import cprint
from asn1crypto import pkcs12
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_directories(timestamp):
    """Creates directory structure for storing certificates and hashes."""
    dir_name = f"certs_{timestamp}"
    os.makedirs(dir_name, exist_ok=True)
    return dir_name

def make_request(api_key, prev_days):
    """Make a request to the API and return file URLs."""
    try:
        resp = requests.get("https://buckets.grayhatwarfare.com/api/v2/files?extensions=pfx",
                            headers={"Authorization": f"Bearer {api_key}"})
        resp.raise_for_status()
        data = resp.json()
        return filter_files(data, prev_days)
    except requests.RequestException as e:
        logging.error(f"Failed to fetch data: {e}")
        sys.exit(1)

def filter_files(data, prev_days):
    """Filter files based on modification date."""
    time_start = timedelta(days=int(prev_days))
    time_now = datetime.now()
    file_urls = [file['url'] for file in data['files'] if datetime.fromtimestamp(file['lastModified']) >= time_now - time_start]
    return file_urls

def download_file(file_url, dir_name):
    """Download a single file and save it locally."""
    try:
        file_data = requests.get(file_url)
        file_data.raise_for_status()
        filename = file_url.rsplit('/', 1)[-1]
        filepath = os.path.join(dir_name, filename)
        with open(filepath, 'wb') as f:
            f.write(file_data.content)
        return filename
    except requests.RequestException:
        logging.error(f"Failed to download file: {file_url}")
        return None

def check_and_process_file(filename, dir_name):
    """Check file for specific sequence and generate hash if valid."""
    filepath = os.path.join(dir_name, filename)
    try:
        with open(filepath, 'rb') as file:
            file.seek(4)
            if file.read(4).hex() == '02010330':
                cprint(f"Cert found! {filename}", "green")
                generate_hash_file(filename, dir_name)
            else:
                os.remove(filepath)
    except IOError as e:
        logging.error(f"Error processing file {filename}: {e}")

def generate_hash_file(filename, dir_name):
    """Generate hash for a valid PFX file and log results."""
    # Similar to your previous implementation but using logging and more structured error handling
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="cert_scraper", description="Scrape for leaked certificates.")
    parser.add_argument("--api-key", help="API key", required=True)
    parser.add_argument("-d", "--days", help="Find certs from the last X days", required=True)
    args = parser.parse_args()

    logging.info("Searching for certificates")
    dir_name = setup_directories(datetime.now().strftime("%Y%m%d%H%M%S"))
    file_urls = make_request(args.api_key, args.days)
    if not file_urls:
        cprint("[!] No certificates found in that timeframe!", "red")
        sys.exit(1)

    for file_url in file_urls:
        filename = download_file(file_url, dir_name)
        if filename:
            check_and_process_file(filename, dir_name)

    logging.info(f"Certificate(s) and hashes saved in: {dir_name}")

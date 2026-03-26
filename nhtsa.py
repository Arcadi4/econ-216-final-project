# -*- coding: utf-8 -*-

import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed


DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)


AUX_BASE_URL = "https://static.nhtsa.gov/nhtsa/downloads/FARS/{year}/National/FARS{year}NationalAuxiliaryCSV.zip"
FULL_BASE_URL = "https://static.nhtsa.gov/nhtsa/downloads/FARS/{year}/National/FARS{year}NationalCSV.zip"


def download_file(url, filepath, year, filetype):
    print(f"Downloading {filetype} for {year}...")
    try:
        response = requests.get(url, stream=True, timeout=60)
        response.raise_for_status()
        with open(filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print(f"Saved: {filepath}")
    except Exception as e:
        print(f"Failed to download {filetype} for {year}: {e}")


def main():
    tasks = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        for year in range(1975, 2023):
            url_aux = AUX_BASE_URL.format(year=year)
            url_full = FULL_BASE_URL.format(year=year)
            filename_aux = f"FARS{year}NationalAuxiliaryCSV.zip"
            filename_full = f"FARS{year}NationalCSV.zip"
            filepath_aux = os.path.join(DATA_DIR, filename_aux)
            filepath_full = os.path.join(DATA_DIR, filename_full)
            tasks.append(executor.submit(download_file, url_aux,
                         filepath_aux, year, "Auxiliary"))
            tasks.append(executor.submit(
                download_file, url_full, filepath_full, year, "Full"))
        for future in as_completed(tasks):
            pass


if __name__ == "__main__":
    main()

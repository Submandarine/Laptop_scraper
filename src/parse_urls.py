import os
import parse_master_3000 as pm
from bs4 import BeautifulSoup
from structure import *


def parse_to_url_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = f.read()
    if ".txt" in file_path:
        # all items are listed twice for some reason, cut of file
        data = data[: data.index("Gesamtanzahl")]

        item_ids = pm.parse_relative_to(
            data, "Ähnlichen Artikel", v_offset=2, h_offset=60, type="custom", custom_delim=["=", ">"]
        )
    elif ".htm" in file_path:
        soup = BeautifulSoup(data, "html.parser")
        spans = soup.find_all("span", {"data-item-id": True})
        item_ids = list(set([span["data-item-id"] for span in spans]))

    # write parsed data to url file
    if not os.path.exists(p_urls):
        open(p_urls, "w").close()  # Create an empty file
    with open(p_urls, "r+", encoding="utf-8") as f:
        url_file = f.read()
        for item_id in item_ids:
            if item_id not in url_file:
                f.write(f"https://www.ebay.de/itm/{item_id}\n")

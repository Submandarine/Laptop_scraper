import parse_urls as pu
import parse_data as pd
import database as db
import os
from datetime import datetime
from structure import *


def main():
    # update url list in case user put new txt file
    for filename in os.listdir(p_input_dir):
        file_path = os.path.join(p_input_dir, filename)
        if os.path.isfile(file_path):  # Check if it is a file
            if ".txt" in file_path or ".htm" in file_path:
                print(f'gathering urls from file "{file_path}"')
                pu.parse_to_url_file(file_path)

    with open(p_urls, "r+", encoding="utf-8") as f:
        urls = f.readlines()

    # check if database exists
    if not os.path.exists(p_database):
        # Create database
        with open(p_database, "w") as f:
            f.write("name,price,shipping,ram,disk,cpu,cpu_mark,url,online")

    # check database entries older than 1 day
    db.update_older_than(1)

    # parse infos from sites not present in database
    with open(p_database, "r+", encoding="utf-8") as f:
        content = f.read()

        for i in range(len(urls)):
            url = urls[i]
            url = url.strip()
            timestamp = datetime.now().isoformat()
            if url not in content:
                print(f"processing url {i}/{len(urls)}")
                # parse
                try:
                    name, price, shipping, ram, disk, cpu, cpu_mark, online = pd.download_and_parse(url)
                    f.write(f"\n{name},{price},{shipping},{ram},{disk},{cpu},{cpu_mark},{url},{online},{timestamp}")
                except Exception:
                    # add as offline so it doesnt get parsed again
                    f.write(f"\nNone,None,None,None,None,None,None,{url},0,{timestamp}")

    import plot


if __name__ == "__main__":
    main()

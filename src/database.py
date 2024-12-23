import csv
import numpy as np
from datetime import datetime, timedelta
import parse_data as pd
from structure import *


class CsvRow:
    def __init__(self, name, price, shipping, ram, disk, cpu, cpu_mark, url, online, timestamp):
        self.name = name
        self.price = price
        self.shipping = shipping
        self.ram = ram
        self.disk = disk
        self.cpu = cpu
        self.cpu_mark = cpu_mark
        self.url = url
        self.online = online
        self.timestamp = timestamp


# shorthand for rows just use c.price
c = CsvRow(name=0, price=1, shipping=2, ram=3, disk=4, cpu=5, cpu_mark=6, url=7, online=8, timestamp=9)


def read_database_to_np():
    data = []
    with open(p_database, "r", encoding="utf-8") as csvfile:
        rows = csv.reader(csvfile, delimiter=",")
        for row in rows:
            # only load intact rows
            if len(row) == 10:
                data.append(np.array(row))
    data = np.array(data[1:])  # remove header
    return data


# overwrites file if present
def write_np_to_database(array):
    with open(p_database, "w", encoding="utf-8") as f:
        f.write("name,price,shipping,ram,disk,cpu,cpu_mark,url,online,timestamp")
        for line in array:
            f.write(
                f"\n{line[c.name]},{line[c.price]},{line[c.shipping]},{line[c.ram]},{line[c.disk]},{line[c.cpu]},{line[c.cpu_mark]},{line[c.url]},{line[c.online]},{line[c.timestamp]}"
            )


def update_older_than(days):
    data = read_database_to_np()
    for entry in data:
        timestamp = datetime.fromisoformat(entry[c.timestamp])
        cutoff_time = datetime.now() - timedelta(days=days)
        if timestamp < cutoff_time:
            print(f"updating database entry {entry[c.name]}")
            name, price, shipping, ram, disk, cpu, cpu_mark, online = pd.download_and_parse(entry[c.url])
            entry[c.name] = name if name != "None" else entry[c.name]
            entry[c.price] = price if price != "None" else entry[c.price]
            entry[c.shipping] = shipping if shipping != "None" else entry[c.shipping]
            entry[c.ram] = ram if ram != "None" else entry[c.ram]
            entry[c.disk] = disk if disk != "None" else entry[c.disk]
            entry[c.cpu] = cpu if cpu != "None" else entry[c.cpu]
            entry[c.cpu_mark] = cpu_mark if cpu_mark != "None" else entry[c.cpu_mark]
            entry[c.online] = online
            entry[c.timestamp] = datetime.now().isoformat()
    write_np_to_database(data)

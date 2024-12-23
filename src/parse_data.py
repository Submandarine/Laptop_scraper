import urllib.request, urllib.error, urllib.parse
import parse_master_3000 as pm
from bs4 import BeautifulSoup
import DSParse_helper as ds


def download_and_parse(url):
    response = urllib.request.urlopen(url)
    webContent = response.read().decode("UTF-8")
    return parse_txt(webContent)


def parse_file(file):
    with open(file, "r", encoding="utf-8") as f:
        data = f.read()
        parse_txt(data)


def parse_txt(data):
    soup = BeautifulSoup(data, "html.parser")

    try:
        name = soup.find("h1", class_="x-item-title__mainTitle").text.strip().replace(",", " ")
        name = name.replace("\n", "")
        name = name.replace("  ", " ")
    except Exception:
        name = "None"

    try:
        disk = soup.find("dl", class_="ux-labels-values--festplattenkapazität").find("dd").find("div").text.strip()
        if "GB" in disk:
            disk = pm.parse_relative_to(disk, "GB", 0, -2, "int", on_error="fill", error_fill="0")[0]
        elif "TB" in disk:
            disk = int(pm.parse_relative_to(disk, "TB", 0, -2, "int", on_error="fill", error_fill="0")[0]) * 1024
        else:
            disk = "0"
    except Exception:
        disk = "0"

    try:
        ram = soup.find("dl", class_="ux-labels-values--arbeitsspeichergröße").find("dd").find("div").text.strip()
        ram = pm.parse_relative_to(ram, "GB", 0, -2, "int", "fill", "0")[0]
        if ram == "0":
            # xx GB not found, try xxGB
            ram = pm.parse_relative_to(ram, "GB", 0, -1, "int", "fill", "0")[0]
    except Exception:
        ram = "0"

    try:
        cpu = soup.find("dl", class_="ux-labels-values--prozessor").find("dd").find("div").text.strip()
        cpu, cpu_mark = ds.get_cpu_type(cpu)
        if cpu_mark == "None":
            # try to find in title instead
            cpu, cpu_mark = ds.get_cpu_type(name)
    except Exception:
        cpu = cpu_mark = "None"

    try:
        price = soup.find("div", class_="vim x-bin-price").text.strip()
        price = pm.conv_german_to_float(pm.parse_relative_to(price, "EUR", 0, 5, "float_german")[0])
    except Exception:
        price = "None"

    # detect if offer still online (content stays parsable after for some time after being taken down)
    online = 1
    if "Dieses Angebot wurde vom Verkäufer" in data:
        online = 0

    return (name, price, "None", ram, disk, cpu, cpu_mark, online)

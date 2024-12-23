import urllib.request, urllib.error, urllib.parse

# specify how many results to load
limit = 100000
url = "https://www.ebay.de/itm/176752538950"

response = urllib.request.urlopen(url)
webContent = response.read().decode("UTF-8")
with open("test.htm", "w+", encoding="utf-8") as f:
    f.write(webContent)

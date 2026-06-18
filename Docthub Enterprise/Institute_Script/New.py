import html

import lxml
import requests

url = "https://www.docthub.com/"
response = requests.get(url)

tree = html.fromstring(response.content)
links = tree.xpath('//a[@href]/@href')

print(links)
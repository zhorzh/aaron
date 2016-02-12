import requests
import json
from pprint import pprint
from lxml.etree import HTML

urls = []
for i in range(0, 843):
    urls.append('https://public.resource.org/aaron/pub/msg{}.html'
                .format(str(i).rjust(5, '0')))


def request_page(url):
    response = requests.get(url)
    text = response.text.encode('utf-8').split('<hr>')
    headers_html = HTML(text[1])
    body_html = HTML('<div>' + text[2] + '</div>')
    return headers_html, body_html


def parse(headers_html, body_html):
    headers = headers_html.xpath("string(//ul)").split('\n')
    header_from = 'no such field'
    for header in headers:
        if 'To: ' in header:
            header_to = header[4:]
        if 'From: ' in header:
            header_from = header[6:]
        if 'Date: ' in header:
            header_date = header[6:]

    body = body_html.xpath("string(//div)").split('\n')
    body = ' '.join(body).strip()

    return {'To': header_to,
            'From': header_from,
            'Date': header_date,
            'Body': body}


results = []
pprint(urls)
for url in urls:
    headers_html, body_html = request_page(url)
    items = parse(headers_html, body_html)
    pprint(items)
    results.append(items)

with open('data.json', 'w') as fp:
    json.dump(results, fp)

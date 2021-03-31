from http.server import HTTPServer, SimpleHTTPRequestHandler
import pandas
from collections import defaultdict
from jinja2 import Environment, FileSystemLoader, select_autoescape
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("echo")
args = parser.parse_args()

excel_data_df = pandas.read_excel(
    f'{args.echo}.xlsx',
    na_values=['N/A', 'NA'],
    keep_default_na=False
)
wines = excel_data_df.to_dict(orient='records')
groups_wines = defaultdict(list)
for wine in wines:
    groups_wines[wine['Название']].append(wine)

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)
template = env.get_template('index.html')
rendered_page = template.render(wines=wines)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()

import os
import pandas as pd
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler

from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader, select_autoescape



def convert_year_text(work_years):
	if work_years % 10 == 1 and work_years != 11 and work_years % 100 != 11:
		return 'год'
	elif 1 < work_years % 10 <= 4 and work_years != 12 \
			and work_years != 13 and work_years != 14:
		return 'года'
	else:
		return 'лет'


def create_product_dict(products_file):
	data_frame = pd.read_excel(io=products_file,
	                           sheet_name='Лист1',
	                           names=['category', 'title', 'sort', 'price', 'image', 'offer'],
	                           keep_default_na=False,
	                           )
	products_dict = dict(data_frame.set_index('category').groupby('category'). \
	                     apply(lambda x: x.to_dict(orient='records')))
	return products_dict


def render_page(products_file):
	template = env.get_template('template.html')
	work_years = int((datetime.now() - datetime(year=1920, month=1, day=1)).days / 365)
	rendered_page = template.render(
		year=work_years,
		year_text=convert_year_text(work_years),
		products_data=create_product_dict(products_file),
	)

	with open('index.html', 'w', encoding="utf8") as file:
		file.write(rendered_page)


if __name__ == '__main__':
	load_dotenv()
	products_file = os.getenv('PRODUCTS_FILE')

	env = Environment(
		loader=FileSystemLoader('.'),
		autoescape=select_autoescape(['html', 'xml'])
	)

	render_page(products_file)
	server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
	server.serve_forever()

from bs4 import BeautifulSoup
from os import listdir
from os.path import isfile, join
import pandas as pd
from pandas import ExcelWriter
import save_article_xml as xmls



def properly_formatted_table(table):
	prev_row_length = 0
	table_rows = table.find_all('row')
	for tr in table_rows:
		row_data = tr.find_all("entry")
		row = [data.text.strip() for data in row_data]
		if prev_row_length != 0:
			if len(row) != prev_row_length:
				return False
		prev_row_length = len(row)

	return True


def scrape_table_data(files):
	writer = ExcelWriter('extracted_tables_better_all_articles.xlsx')
	total_tables = 0
	bad_tables = 0
	all_tables = []
	for file in files:
		with open(file) as f:
			xml_doc = f.read()
		soup = BeautifulSoup(xml_doc, "lxml-xml")
		tables = soup.find_all('table')
		title = soup.find('title')
		title = title.text.strip()
		for i, table in enumerate(tables):
			total_tables += 1
			if not properly_formatted_table(table):
				#print("table {}".format(total_tables), "not formatted prpoperly")
				bad_tables += 1
				continue
			l = []
			l.append(["article:", title])
			table_rows = table.find_all('row')
			for tr in table_rows:
				td = tr.find_all('entry')
				row = [data.text.strip().replace("\n", " ") for data in td]
				if len(row) != 0:
					l.append(row)
			df = pd.DataFrame(l)
			df.to_excel(writer,'table{}'.format(total_tables))
			writer.save()
			all_tables.append(df)
	'''
	print("total tables:", total_tables)
	print("bad tables:", bad_tables)
	print("percentage bad tables:", round(float(bad_tables / total_tables * 100), 2), "%")
	'''
	return all_tables


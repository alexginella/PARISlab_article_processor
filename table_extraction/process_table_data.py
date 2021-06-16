from table_extraction import extract_tables_xml as scraper
from os import listdir
from os.path import isfile, join
import pandas as pd
from pandas import ExcelWriter
from table_extraction import compile_table_data as data_compiler

#tables talking about oxides in columns only
def tables_of_interest(tables):
	interesting_tables = []
	for table in tables:
		col_names = data_compiler.find_column_names(table)
		if "Al2O3" in col_names:
			interesting_tables.append(table)
			#table contains oxides
	return interesting_tables

def material_lookup_table(tables):
	tables = tables_of_interest(tables)
	material_to_tables = {}
	for table in tables:
		materials = list(table.iloc[:,0])[2:] #we dont want the column names or article name so omit the first two rows
		for material in materials:
			try: 
				material_to_tables[material].append(table)
			except:
				material_to_tables[material] = [table]
	return material_to_tables


def pair_material_to_data(tables):
	lookup_table = material_lookup_table(tables)
	mats = lookup_table.keys()
	material_to_data = {}
	for material in mats:
		tables = lookup_table[material]
		for table in tables:
			column_names = table.iloc[1]
			#print("material:", material, '\tcolumn names:', column_names)


def process_tables(onlyfiles):
	#onlyfiles = [onlyfiles[-1]]
	for file in onlyfiles:
		#scrape tables from xml of file
		tables = scraper.scrape_table_data(file)
		lookup_table = material_lookup_table(tables)
		data_compiler.compile_to_one_table(lookup_table, tables)		


if __name__ == '__main__':
	get_tables()

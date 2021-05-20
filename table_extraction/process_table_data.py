from table_extraction import extract_tables_xml as scraper
from os import listdir
from os.path import isfile, join
import pandas as pd
from pandas import ExcelWriter
from table_extraction import compile_table_data as data_compiler


def material_lookup_table(tables):
	material_to_tables = {}
	for table in tables:
		materials = table.iloc[:,0]
		materials = materials[1:]
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


def process_tables():
	mypath = "./xml-files"
	onlyfiles = [join(mypath,f) for f in listdir(mypath) if isfile(join(mypath, f))]
	print("processing tables from:", onlyfiles)
	onlyfiles = [onlyfiles[0]]
	for file in onlyfiles:
		#scrape tables from xml of file
		tables = scraper.scrape_table_data(file)
		lookup_table = material_lookup_table(tables)
		data_compiler.compile_to_one_table(lookup_table)		


if __name__ == '__main__':
	get_tables()

import extract_tables_xml as scraper
from os import listdir
from os.path import isfile, join
import pandas as pd
from pandas import ExcelWriter


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


def get_tables():
	#piis = ["S0008884619311421", "S0950061820301434", "S0008884619316515", "S0958946514001863", "S0958946516302517", "S0008884611002274", "S0950061819316277"]	
	#xmls.get_xml(piis)
	mypath = "./xml-files"
	onlyfiles = [join(mypath,f) for f in listdir(mypath) if isfile(join(mypath, f))]
	print(onlyfiles)
	tables = scraper.scrape_table_data(onlyfiles)
	table = material_lookup_table(tables)
	writer = ExcelWriter("CaO_tables.xlsx")
	cao_tables = table["CaO"]
	for i, table in enumerate(cao_tables):
		table.to_excel(writer,'table{}'.format(i))
		writer.save()
	#pair_material_to_data(tables)

if __name__ == '__main__':
	get_tables()

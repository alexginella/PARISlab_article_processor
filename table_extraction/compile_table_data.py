import pandas as pd
from pandas import ExcelWriter

def find_column_names(table):
	row_number = 1
	column_names = list(table.iloc[row_number])
	#make sure we dont get all Nones
	if len(column_names) == column_names.count(None):
		row_number += 1
		column_names = table.iloc[row_number]
	return column_names

def create_column_buckets(tables):
	column_name_to_number = {}
	column_number = 1  #starting in the second column cause first has material names
	for table in tables:
		column_names = find_column_names(table)
		for name in column_names[1:]: #first name is the label of the material (ID, Compound, etc)
			if (name) and (not name in column_name_to_number.keys()): #unique column names
				column_name_to_number[name] = column_number
				column_number += 1
	return column_name_to_number

def compile_to_one_table(lookup_table, tables):
	writer = ExcelWriter("./table_extraction/compiled_article1_test1.xlsx")
	materials = set(lookup_table.keys()) #all unique materials 
	map_col_name_to_index = create_column_buckets(tables)

	compiled_table = []

	top_row = [None] * (len(map_col_name_to_index.keys()) + 1) #plus 1 so we can add the name of the material too
	top_row[0] = "item (type)"
	compiled_table.append(top_row)

	for material in materials:
		tables = lookup_table[material]
		row = [None] * len(top_row) 
		for table in tables:
			material_row_number = list(table.iloc[:,0]).index(material) #row containing data for material
			column_names = find_column_names(table)
			material_row = list(table.iloc[material_row_number])
			if column_names[0]:
				material_name_and_type = material_row[0] + " (" + column_names[0] + ")"
			else:
				material_name_and_type = material_row[0]
			values_and_type = [(val, name) for name, val in zip(column_names[1:], material_row[1:])]
			row[0] = material_name_and_type
			for data in values_and_type:
				index = map_col_name_to_index[data[1]]
				compiled_table[0][index] = data[1] #ensure the column names and data match up
				row[index] = data[0]
			compiled_table.append(row)

	df = pd.DataFrame(compiled_table)
	df.to_excel(writer)
	writer.save()

#ask, what happens when there are two tables that have different
#values under the same column name for the same material/oxide/whatever?
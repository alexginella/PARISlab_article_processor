import pandas as pd

def compile_to_one_table(lookup_table):
	materials = set(lookup_table.keys())
	#print(materials)
	material = list(materials)[7]
	print(material)
	tables = lookup_table[material]
	print(tables)
	for table in tables:
		material_row = list(table.iloc[:,0]).index(material)
		#print(table.iloc[0])
		print(table.iloc[material_row])
	

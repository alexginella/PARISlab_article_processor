from os import listdir
from os.path import isfile, join
import pandas as pd
from pandas import ExcelWriter
import pandas_read_xml as pdx


mypath = "./xml-files/"
onlyfiles = [mypath + f for f in listdir(mypath) if isfile(join(mypath, f))]
file = onlyfiles[0]
#print(file)
#with open(file) as f:
#	dfs = pd.read_html(f)
#print(r.status_code)
#dfs = pdx.read_xml("output.xml", ['ce:table'])
dfs = pd.read_html(file)
print(dfs)
writer = ExcelWriter('extracted_tables.xlsx')
for i, table in enumerate(dfs):
	table.to_excel(writer,'table{}'.format(i+1))
	writer.save()

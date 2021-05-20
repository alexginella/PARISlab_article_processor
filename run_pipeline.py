#import generate_knowledge_graph
#import generate_tuples
import clean_article_text
import structure_sentence
from table_extraction import process_table_data
import sys


def err_msg():
	print("Usage: add -t command line parameter to use table approach")
	print("       add -nlp command line parameter to use nlp+table approach")
	exit()


def nlp_approach():
	filename = "json-files/article0.json"
	print("processing file:", filename)
	sentences = clean_article_text.produce_filtered_sentence_data(filename)[0]
	process_table_data.get_tables()
	tuples = []
	for sentence in sentences:
		sen = structure_sentence.Structure_Sentence(sentence)
		obj = sen.json_object
		#tp = generate_tuples.remove_empty_tuples(tp)
		#entity_pairs = generate_tuples.one_to_one_mapping(res)
		tuples += obj
	
	for tp in tuples:
		if tp != ([],[],[],[]):
			print(tp)


def table_approach():
	process_table_data.process_tables()




def main():
	args = sys.argv
	if len(args) == 1 or len(args) > 2:
		err_msg()

	flag = args[1]
	if flag == "-nlp":
		nlp_approach()		
	elif flag == "-t":
		table_approach()
	else:
		err_msg()


if __name__ == '__main__':
	main()
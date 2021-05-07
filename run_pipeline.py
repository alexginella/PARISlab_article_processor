#import generate_knowledge_graph
#import generate_tuples
import clean_article_text
import structure_sentence
from table_extraction import process_table_data

def main():
	
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



if __name__ == '__main__':
	main()
import spacy
from spacy.matcher import Matcher 
from spacy import displacy
import en_core_web_sm
nlp = en_core_web_sm.load()


class Structure_Sentence():

	"""docstring for Structure_Sentence"""
	def __init__(self, sentence):
		self.tuples = self.generate_tuples(sentence)[1]
		self.json_object = self.get_objects(sentence)
	

	def get_relation(self, sent):
	    """ Get the Root of the sentence """
	    doc = nlp(sent)

	    # Matcher class object 
	    matcher = Matcher(nlp.vocab)

	    #define the pattern 
	    pattern = [{'DEP':'ROOT'}, 
	               {'DEP':'prep','OP':"?"},
	               {'DEP':'agent','OP':"?"},  
	               {'POS':'ADJ','OP':"?"}] 

	    matcher.add("matching_1", None, pattern) 	#problematic

	    matches = matcher(doc)
	    k = len(matches) - 1

	    span = doc[matches[k][1]:matches[k][2]] 

	    return(span.text)


	def split_numbers(self, text, unit):
	    """ Split numbers and map to their units """
	    conjunctions = []
	    splits = [number for number in text.split() if number.isdigit()]
	    if splits != []:
	        numbers = [number + " " + unit for number in splits]
	        conjunctions.extend(numbers)
	    return conjunctions


	def find_conjunctions(self, pos, noun_chunks):
	    """ Find related conjunctions """
	    conjunctions = []; store = True;
	    
	    # -- Split numbers if any in the root object
	    splits = self.split_numbers(noun_chunks[pos]["text"], noun_chunks[pos]["root"])
	    if splits != [] and noun_chunks[pos]["root_dep"].find("subj") == -1:
	        conjunctions.extend(splits)
	        store = False
	                
	    for i, chunk in enumerate(noun_chunks):
	        if i <= pos: continue
	        if not chunk["root_dep"].endswith("conj"): break
	        else:
	            # -- If the original noun chunk is not fully composed, update it
	            updated = noun_chunks[pos]["text"]
	            if noun_chunks[pos]["text"].find(chunk["root"]) == -1:
	                updated += (" " + chunk["root"])
	            
	            # -- Store original only once
	            if not updated in conjunctions and store:
	                conjunctions.append(updated)
	                
	            # -- Split numbers
	            splits = self.split_numbers(chunk["text"], chunk["root"])
	            if splits != [] and chunk["root_dep"].find("subj") == -1:
	                conjunctions.extend(splits)
	                continue
	                
	            # -- Store the consecutive conjunctions
	            conjunctions.append(chunk["text"])
	            
	        # -- If no conjunctions,then return original text only
	    if conjunctions == []:
	        conjunctions.append(noun_chunks[pos]["text"])
	    
	    return conjunctions



	def init_tuple(self):
	    """ Helper function to initialize new tuple """
	    return ([], [], [], [])


	def generate_tuples(self, sentence):
	    """ Generate the above tuples """
	    doc = nlp(sentence)
	    
	    # -- Map noun chunks 
	    noun_chunks = []
	    for chunk in doc.noun_chunks:
	        derived = {"text": chunk.text, "root": chunk.root.text, "root_dep": chunk.root.dep_, "root_head": chunk.root.head, "root_head_dep": chunk.root.head.dep_}
	        noun_chunks.append(derived)
	        
	    subjects = []; objects = []; attributes = [];
	    relation = ""
	    tuples = []; count = 0; new_tuple = self.init_tuple();
	    
	    # -- Get all entities in the sentence
	    for i,chunk in enumerate(noun_chunks):
	        # -- One set of relations found, onto the next
	        if count == 4: 
	            # - Reinitialize everything
	            count = 0
	            tuples.append(new_tuple)
	            new_tuple = self.init_tuple()
	            
	        # -- Get the subjects
	        if chunk["root_dep"].find("subj") != -1:
	            conjections = self.find_conjunctions(i, noun_chunks)
	            subjects.extend(conjections)
	            # - Reinitialize everything
	            count = 0
	            tuples.append(new_tuple)
	            new_tuple = self.init_tuple()
	            new_tuple[0].extend(conjections)
	            count += 1
	                
	            
	            
	        # -- Get the objects
	        elif chunk["root_dep"].find("obj") != -1:
	            conjections = self.find_conjunctions(i, noun_chunks)
	            objects.extend(conjections)
	            
	            ans = ""
	            for a in chunk["root_head"].ancestors:
	                ans = a
	                break
	                
	            if ans.pos_ == "ADP":
	                ans_of_ans = ""
	                for b in ans.ancestors:
	                    ans_of_ans = b
	                    break
	                    
	                relation = ans_of_ans.text + " " + ans.text + " " + chunk["root_head"].text
	                new_tuple[2].extend([relation])
	                count += 1
	                    
	            elif chunk["root_head"].pos_ == "ADP":
	                ans = chunk["root_head"]
	                ans_of_ans = ""
	                for b in ans.ancestors:
	                    ans_of_ans = b
	                    break
	                    
	                relation = ans_of_ans.text + " " + ans.text + " " + chunk["root_head"].text
	                new_tuple[2].extend([relation])
	                count += 1
	            new_tuple[1].extend(conjections)
	            count += 1
	            
	        # -- Get the attributes
	        elif chunk["root_dep"].find("attr") != -1:
	            conjections = self.find_conjunctions(i, noun_chunks)
	            attributes.extend(conjections)
	            new_tuple[3].extend(conjections)
	            count += 1
	    
	    tuples.append(new_tuple)
	    # -- Get the relation in the sentence
	    relation = ""#self.get_relation(sentence)
	    return {"subjects": subjects, "objects": objects, "relation": relation, "attributes": attributes}, tuples



	def get_objects(self, sentence):
	    """ Extract Noun Chunks """
	    doc = nlp(sentence)
	    
	    # -- Map noun chunks 
	    noun_chunks = []
	    for chunk in doc.noun_chunks:
	        derived = {"text": chunk.text, "root": chunk.root.text, "root_dep": chunk.root.dep_}
	        noun_chunks.append(derived)
	    
	    subjects = []; objects = []; attributes = [];
	    relation = ""
	    # -- Get all entities in the sentence
	    for i,chunk in enumerate(noun_chunks):
	        # -- Get the subjects
	        if chunk["root_dep"].find("subj") != -1:
	            conjections = self.find_conjunctions(i, noun_chunks)
	            subjects.extend(conjections)
	            
	        # -- Get the objects
	        elif chunk["root_dep"].find("obj") != -1:
	            conjections = self.find_conjunctions(i, noun_chunks)
	            objects.extend(conjections)
	            
	        # -- Get the attributes
	        elif chunk["root_dep"].find("attr") != -1:
	            conjections = self.find_conjunctions(i, noun_chunks)
	            attributes.extend(conjections)
	    
	    # -- Get the relation in the sentence
	    relation = "" #self.get_relation(sentence)
	    return {"subjects": subjects, "objects": objects, "relation": relation, "attributes": attributes}, noun_chunks

	

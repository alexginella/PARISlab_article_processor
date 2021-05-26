import spacy
from spacy.matcher import Matcher 
from spacy import displacy
import en_core_web_sm
nlp = en_core_web_sm.load()

import SpacyAnalyzer as SA
from Libraries import *


class TupleGenerator():
    ''' Main class: transform articles and list of tuples '''
    def __init__(self):
        pass
        
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

        matcher.add("matching_1", None, pattern) 

        matches = matcher(doc)
        k = len(matches) - 1

        try:
            span = doc[matches[k][1]:matches[k][2]] 

            return(span.text)
        except:
            return ""
        
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
            
        # -- Find the root of the noun chunks
        root = ""
        for i, chunk in enumerate(noun_chunks):
            if i <= pos: continue
            if not chunk["root_dep"].endswith("conj"): break
            root = chunk["root"]
                    
        for i, chunk in enumerate(noun_chunks):
            if i <= pos: continue
            if not chunk["root_dep"].endswith("conj"): break
            else:
                # -- If the original noun chunk is not fully composed, update it
                updated = noun_chunks[pos]["text"]
                if noun_chunks[pos]["text"].find(root) == -1:
                    updated += (" " + root)
                
                # -- Store original only once
                if not updated in conjunctions and store:
                    conjunctions.append(updated)
                    
                # -- Split numbers
                splits = self.split_numbers(chunk["text"], root)
                if splits != [] and chunk["root_dep"].find("subj") == -1:
                    conjunctions.extend(splits)
                    continue
                    
                # -- Store the consecutive conjunctions
                updated_conj = f'{chunk["text"]} {root}' if (chunk["text"].find(root) == -1) else chunk["text"]
                conjunctions.append(updated_conj)
                
            # -- If no conjunctions,then return original text only
        if conjunctions == []:
            conjunctions.append(noun_chunks[pos]["text"])
        
        return conjunctions 
        
    def filter_out(self, build_up):
        """ Helper to Combine Mods """
        seen = set()
        return " ".join([token for token in build_up if not (token in seen or seen.add(token))])
        
    def combine_mods(self, sentence):
        """ Combine All Entities with their modifiers """
        sentence = sentence.lower()
        entities = {"subjects": [], "objects": [], "attributes": [], "relation": ""}
        doc = nlp(sentence)
        build_up = []; left_off = [];
        for i,token in enumerate(doc):
            try:
                # -- If it is a modifier and its head is the next word, combine them
                if token.dep_.endswith("mod") and token.head.text == doc[i+1].text:
                    build_up.extend([token.text, token.head.text])
                    left_off = []

                # -- If the head of the modifier is far away
                elif token.dep_.endswith("mod"):
                    left_off.extend([token.text])

                # -- Marks the end, when a non modifier is next
                elif token.head.text == doc[i+1].text:
                    build_up.extend(left_off)
                    build_up.extend([token.text])
                    build_up = filter_out(build_up)

                    if token.dep_.find("subj") != -1:
                        entities["subjects"].append(build_up)
                    if token.dep_.find("obj") != -1:
                        entities["objects"].append(build_up)
                    if token.dep_.find("attr") != -1:
                        entities["attributes"].append(build_up)

                    build_up = []; left_off = [];
            except:
                pass
            
        return entities
        
    def add_missed_chunks(self, sentence, parsed):
        """ Add the missed noun chunks manually """
        entities = self.combine_mods(sentence)
        for key,value in entities.items():
            # -- Add here if not exists already
            if value not in parsed[key]:
                parsed[key].extend(value)
        # -- Return new version
        return parsed
        
    def get_objects(self, sentence):
        """ Extract Noun Chunks """
        sentence = sentence.lower()
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
        relation = self.get_relation(sentence)
        return {"subjects": subjects, "objects": objects, "relation": relation, "attributes": attributes}, noun_chunks
        
    def display_information(self, sentence):
        """ Display all information about a sentence and its parsing """
        parsed, noun_chunks = self.get_objects(sentence)
        
        # -- Add missed chunks by spacy
        parsed = self.add_missed_chunks(sentence, parsed)
        
        pp = pprint.PrettyPrinter(indent=2)
        generate_tables(sentence)
        print("-------")
        pp.pprint(parsed)
        SA.generate_syntax_trees([sentence])
        
    def init_tuple(self):
        """ Helper function to initialize new tuple """
        return ([], [], [], [])
        
    def get_first_ancestor(self, chunk):
        """ Get the first ancestor of a given chunk """
        try:
            for ancestor in chunk.ancestors:
                return ancestor
        except:
            return None
        
    def generate_tuples(self, sentence):
        """ Generate the above tuples """
        sentence = sentence.lower()
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
                tuples.append(new_tuple)
                new_tuple = self.init_tuple()
                count = 0
                
            # -- Get the subjects
            if chunk["root_dep"].find("subj") != -1:
                conjections = self.find_conjunctions(i, noun_chunks)
                subjects.extend(conjections)
                
                # - Reinitialize everything upon new subject
                tuples.append(new_tuple)
                new_tuple = self.init_tuple()
                new_tuple[0].extend(conjections)
                count = 1
                    
                
                
            # -- Get the objects and relations
            elif chunk["root_dep"].find("obj") != -1:
                conjections = self.find_conjunctions(i, noun_chunks)
                objects.extend(conjections)
                
                try:
                    first_ancestor = self.get_first_ancestor(chunk["root_head"])

                    # -- If the ancestor of the object is a preposition, get what's before it
                    if first_ancestor.pos_ == "ADP":
                        second_ancestor = self.get_first_ancestor(first_ancestor)

                        # -- In this case, this object is a relation
                        relation = f'{second_ancestor.text} {first_ancestor.text} {chunk["root_head"].text}'

                        # -- Append to the relation column of the tuple
                        new_tuple[2].extend([relation])
                        count += 1

                    # -- If the chunk root itsel is the preposition
                    elif chunk["root_head"].pos_ == "ADP":
                        first_ancestor = self.get_first_ancestor(chunk["root_head"])

                        # -- In this case, this object is a relation
                        relation = f'{first_ancestor.text} {chunk["root_head"].text}'

                        # -- Append to the relation column of the tuple
                        new_tuple[2].extend([relation])
                        count += 1
                except:
                    pass
                    
                # -- Append to the objects column of the tuple
                new_tuple[1].extend(conjections)
                count += 1
                
            # -- Get the attributes
            elif chunk["root_dep"].find("attr") != -1:
                conjections = self.find_conjunctions(i, noun_chunks)
                attributes.extend(conjections)
                
                # -- Append to tuple attributes column
                new_tuple[3].extend(conjections)
                count += 1
        
        tuples.append(new_tuple)
        # -- Get the relation in the sentence
        relation = self.get_relation(sentence)
        return {"subjects": subjects, "objects": objects, "relation": relation, "attributes": attributes}, tuples
        
        
        
        
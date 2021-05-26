import spacy
from spacy.matcher import Matcher 
from spacy import displacy
import en_core_web_sm
nlp = en_core_web_sm.load()

from Libraries import *


class TupleEnhancer():
    ''' Template class: More in-depth analysis of tuples '''
    def __init__(self):
        pass
        
    def init_tuple(self):
        """ Helper function to initialize new tuple """
        return ([], [], [], [])
        
    def one_to_one_mapping(self, tup):
        """ If a 1-1 mapping exists then extract the tuples """
        subjects, objects, relation, attributes = tup[0], tup[1], tup[2], tup[3]
        subj_len, obj_len, rel_len, attr_len = len(subjects), len(objects), len(relation), len(attributes)
        
        tuples = []
        # -- Case of perfect 1-1 mapping between all columns of tuple
        if subj_len == obj_len:
            for subject,objecct in zip(subjects, objects):
                new_tuple = self.init_tuple()
                new_tuple[0].append(subject)
                new_tuple[1].append(objecct)
                new_tuple[2].extend(relation)
                tuples.append(new_tuple)
            
            if attr_len == len(tuples):
                for i,attr in enumerate(attributes):
                    tuples[i][3].append(attr)
            else:
                # -- If no 1-1 for attributes, assume they refer to same data
                for atup in tuples:
                    atup[3].extend(attributes)
                    
        elif attr_len == obj_len:
        # -- Case of 1 subject, many objects and many attributes
            for attribute,objecct in zip(attributes, objects):
                new_tuple = self.init_tuple()
                new_tuple[3].append(attribute)
                new_tuple[1].append(objecct)
                new_tuple[2].extend(relation)
                tuples.append(new_tuple)
            
            if subj_len == 1:
                for i in range(len(tuples)):
                    tuples[i][0].append(subjects[0])
                    
        else:
            tuples = [tup] # [tup]
            
        return tuples
        
    def is_one2one_tuple(self, tup):
        """ Check if a given tuple is valid """
        return (len(tup[1]) == 1 and len(tup[1]) == 1 and len(tup[1]) == 1 and len(tup[1]) == 1)
        
    def validate_tuple(self, tup, is_one2one=True):
        """ Validate tuples """
        if is_one2one:
            """ Simpler case of one2one tuples """
            new_tup = self.init_tuple()
            # -- Move all number attributes from object to attribute column if any
            numbers = [attr for attr in tup[1] for number in attr.split() if number.isdigit()]
            tup[3].extend(numbers)
            new_tup[3].extend(tup[3])
            
            # -- If relation is subset of attribute, reclassify attribute to relation
            try:
                attribute, relation = tup[3][0].split(), tup[2][0].split()
                swap = False
                for word in relation:
                    # -- Update relation only if prev. relation is subset of attribute
                    if word in attribute: 
                        new_tup[2].extend([" ".join(attribute)])
                        break

                # -- If relation is different than attribute then keep old relation
                if new_tup[2] == []:
                    new_tup[2].extend(tup[2])
            except:
                # -- Case where one of the two is empty
                attribute, relation = tup[3], tup[2]
                if attribute == []:
                    new_tup[3].extend(relation)
                elif relation == []:
                    new_tup[2].extend(attribute)
                    
            # -- Finish constructing the tuple 
            new_tup[0].extend(tup[0])
            new_tup[1].extend([obj for obj in tup[1] if obj not in numbers])
            
            tuples = [new_tup]
            
        else:
            """ Much harder case of tuple columns not being one2one """
             # -- Move all number attributes from object to attribute column if any
            numbers = [attr for attr in tup[1] for number in attr.split() if number.isdigit()]
            tup[3].extend(numbers)
            
            # -- Simpler case: 1-1 mapping between columns
            tuples = self.one_to_one_mapping(tup)
            if tuples == None:
                tuples = [] #other_mapping(tup)

        return tuples
        
    def filter_out_tuples(self, tuples_set):
        """ Filter out the ones with no subjects or objects """
        return [tup for tup in tuples_set if (tup[0] != [] and tup[1] != [] and tup[2] != [])]
        
    def breakdown_tuples(self, tuples):
        """ Given tuples break it down if multiple elements in it """
        tuples_set = []
        # -- Loop through each tuple and treat each case
        for i,tup in enumerate(tuples):
            if self.is_one2one_tuple(tup): 
                valid_tuple = self.validate_tuple(tup, is_one2one=True)
                tuples_set.extend(valid_tuple)
            else:
                valid_tuple = self.validate_tuple(tup, is_one2one=False)
                tuples_set.extend(valid_tuple)
        
        # -- Return the newly formed tuples
        tuples_set = self.filter_out_tuples(tuples_set)
        return tuples_set

    def no_stopwords(self, entity):
        stopwords = nltk.corpus.stopwords.words('english')
        decomp = entity.split(" ")
        filtered = " ".join([word for word in decomp if word not in stopwords])
        return [filtered]
        
    def delete_stop_words(self, tuples):
        result = []
        for tup in tuples:
            subject, objecct, relation, attributes = tup
            
            if len(subject) > 0:
                subject = self.no_stopwords(subject[0])
            if len(objecct) > 0:
                objecct = self.no_stopwords(objecct[0])
            if len(relation) > 0:
                relation = self.no_stopwords(relation[0])
            if len(attributes) > 0:
                attributes = self.no_stopwords(attributes[0])
                
            new_tup = (subject, objecct, relation, attributes)
            result.append(new_tup)
            
        return result
        
        
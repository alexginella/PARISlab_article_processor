import spacy
from spacy.matcher import Matcher 
from spacy import displacy
import en_core_web_sm
nlp = en_core_web_sm.load()

from NLP_Pipeline.Libraries import *

class SpacyAnalyzer():
    ''' Template class: generate spacy tree/tables out of sentences '''
    def __init__(self):
        pass
        
    def generate_tags(self, sentences):
        tables = []
        for sentence in sentences:
            posdocum = nlp(" ".join([word for sent in sentence for word in sent.keys()]))
            table = PrettyTable(['WORD', 'POS', 'TAG'])
            for pair, pos in zip(sentence, posdocum):
                word, tag = list(pair.keys())[0], list(pair.values())[0]
                postag = pos.dep_
                table.add_row([word, postag, tag])
            tables.append(table)
        return tables
        
    def predict_classes(self):
        sentences = []
        with open('temp-data/tags.json', 'r') as f:
            sentences = json.loads(f.read())
        return sentences
        
    def generate_syntax_trees(self, sentences):
        trees_generated = 0
        structures = []
        for sentence in sentences:
            struct = nlp(sentence)
            structures.append(struct)

        svg = displacy.render(structures, style="dep", options={"compact": True, "jupyter": False})
        
    def generate_tables(self, sentence):
        doc = nlp(sentence)
        table = PrettyTable(['TEXT', 'ROOT.TEXT', 'ROOT.DEP_', 'ROOT.HEAD.TEXT'])
        for chunk in doc.noun_chunks:
            table.add_row([chunk.text, chunk.root.text, chunk.root.dep_, chunk.root.head.text])
        print(sentence)
        print(table)
        
    def generate_dep_tree(self, sentence):
        nlp = spacy.load('en_core_web_sm')
        text = nlp(sentence)
        tree = displacy.render(text, style = 'dep', jupyter=False, options={"compact": True})
        save_tree(tree)
        
        
        
        
        
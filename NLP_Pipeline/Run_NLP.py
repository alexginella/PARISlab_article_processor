from NLP_Pipeline import Preprocessing
from NLP_Pipeline import SpacyAnalyzer
from NLP_Pipeline import TupleGenerator
from NLP_Pipeline import TupleEnhancer
from NLP_Pipeline import KnowledgeGraphBuilder as KGBuilder
from os import listdir
from os.path import isfile, join

def launch(sentence, dir_name):
    # -- Example of one sentence 
    #sentence = "Durability is an important performance metric of concrete. Freeze-thaw durability is the most important type of \
    #            durability of concrete. Freeze-thaw durability has a big impact on concrete strength. This freeze-thaw durability \
    #            is largely affected by the small air voids in concrete. These small air voids can release the internal stress in their \
    #            surroundings. As a result, the stress build-up in concrete is reduced. These small air voids are usually intentionally \
    #            entrained into the concrete during fabrication. The diameter of these small air voids is less than 200 um."
                

    if sentence:
        # -- The whole pipeline is to generate tuples
        # - Make enhancements, and removing stop words 
        TG = TupleGenerator.TupleGenerator()
        TH = TupleEnhancer.TupleEnhancer()
        G = KGBuilder.KnowledgeGraphBuilder()
        
        res, tuples = TG.generate_tuples(sentence)
        tuples = TH.breakdown_tuples(tuples)
        tuples = TH.delete_stop_words(tuples)
        
        # -- Display the tuples and generate the Knowledge Graph
        print(tuples)
        G.generate_kg(tuples)
    elif dir_name:
        # -- Example of a full article
        #filename = "../json-files/article0.json"
        print("Processing directory:", dir_name)
        mypath = dir_name
        onlyfiles = [join(mypath,f) for f in listdir(mypath) if isfile(join(mypath, f))]
        for filename in onlyfiles:
            # - Turn the article into a list of sentences
            P = Preprocessing.ArticlePreprocessor()
            sentences = P.produce_filtered_sentence_data(filename)[0]
            
            # - Produce final tuples from each sentence
            final_tuples = []
            for sentence in sentences[27:]:
                res, ttuples = TG.generate_tuples(sentence)
                tp = TH.breakdown_tuples(ttuples)
                tp = TH.delete_stop_words(tp)
                final_tuples.extend(tp)

            # -- Display the tuples and generate the Knowledge Graph
            print(final_tuples)
            G.generate_kg(final_tuples)

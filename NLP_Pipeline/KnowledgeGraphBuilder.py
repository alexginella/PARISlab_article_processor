import bs4
import networkx as nx
import matplotlib.pyplot as plt

from NLP_Pipeline.Libraries import *


class KnowledgeGraphBuilder():
    ''' Template class: for building knowledge graphs out of tuples '''
    def __init__(self):
        pass
        
    def generate_kg(self, entity_pairs):
        """ Given entity pairs, display the knowledge graph """

        # extract subject
        source = [i[0][0] for i in entity_pairs]

        # extract object
        target = [i[1][0] for i in entity_pairs]

        # relations
        try:
            relations = [i[3][0] for i in entity_pairs]
        except:
            relations = [i[2][0] for i in entity_pairs]
            
        kg_df = pd.DataFrame({'source':source, 'target':target, 'edge':relations})
        # create a directed-graph from a dataframe
        G=nx.from_pandas_edgelist(kg_df, "source", "target", 
                                  edge_attr=True, create_using=nx.MultiDiGraph())

        edges = {(src,tar): rel for src,tar,rel in zip(source, target, relations)}
        
        # Display figure 
        plt.figure(figsize=(12,12))
        pos = nx.spring_layout(G)
        nx.draw(G, with_labels=True, node_color='skyblue', edge_cmap=plt.cm.Blues, pos = pos, font_size=14, node_size=1200)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edges, font_color='red', font_size=14)
        plt.show()
        
        return kg_df
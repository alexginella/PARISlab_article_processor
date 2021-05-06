import json
from chemdataextractor import Document
import re
from chemdataextractor.nlp.tokenize import ChemWordTokenizer
import nltk
#nltk.download('stopwords')
# # Data Preprocessing

# ### Data Preprocessing - Functions

def get_raw_sentences(data_file):
    """ Split: document into sentences """
    data = ""
    with open(data_file, 'r', encoding='utf-8') as file:
        data = json.loads(file.read())
    data = data["full-text-retrieval-response"]
    cde_doc = Document(data['originalText'])
    
    sentences = [s.text for s in cde_doc.elements[0].sentences]
    
    return sentences, data['originalText']




def regex_parse_data(data):
    """ Start with a regex parsing of the data """
    non_ascii = data.encode("ascii", "ignore")
    data = non_ascii.decode()
    no_figs = re.sub('\[(.*?)\]',' ', data)
    no_fig2 = re.sub('\((.*?)\)',' ', no_figs)
    #no_punc = re.sub(r'[^\w\s]', ' ', no_figs)
    final = no_fig2
    
    ## Split all values and their units 
    vals = re.findall(".*\d+\.\d+[^0-9 ]+", final)
    splt = [re.split('(\d+\.\d+)', item) for item in vals]
    new_vals = [' '.join(item) for item in splt]
    for i, word in enumerate(vals):
        temp = final.replace(word, new_vals[i])
        final = temp
        
    vals = re.findall(" *\d+[^0-9 .]+", final)
    splt = [re.split('(\d+)', item) for item in vals]
    new_vals = [' '.join(item) for item in splt]
    for i, word in enumerate(vals):
        temp = final.replace(word, new_vals[i])
        final = temp
        
    no_punc = final
    no_comma = re.sub(',', ' ', no_punc)
    no_dash = re.sub('-', ' ', no_comma)
    final = re.sub(' +', ' ', no_dash)

    return final




def extract_relevant_info_from(data):
    """ Gets relevant information from the data file """
    #if not isinstance(data['originalText'], str):
    #    return ""
    data = regex_parse_data(data)
    data = data.lower()
    cwt = ChemWordTokenizer()
    segment = cwt.tokenize(data)
    if segment:
        if segment[len(segment) - 1] == '.':
            segment.pop()
                    
    relevant_data = ""
    start = False

    """ Iterate through each word, record only from abstract to end """
    for word in list(segment):
        relevant_data += str(word)
        relevant_data += " "
            
    tokenized_data = list(segment)
    return relevant_data, tokenized_data


def remove_stop_words(sentences):
    stopwords = nltk.corpus.stopwords.words('english')
    result = []
    filtered = [[word for word in sentence if word not in stopwords] for sentence in sentences]
    return filtered

def produce_filtered_sentence_data(data_file):
    """ Similar to produce_data but applied to sentences """
    article_data, original = get_raw_sentences(data_file)
    sentences = []; tokenized_list = []
    for data in article_data:
        relevant_data, tokenized_data = extract_relevant_info_from(data)
        sentences.append(relevant_data)
        tokenized_list.append(tokenized_data)
    #sentences = remove_stop_words(sentences)
        
    return sentences, tokenized_list, original


from table_extraction import process_table_data
import sys
from os import listdir
from os.path import isfile, join
from NLP_Pipeline import Run_NLP

def err_msg():
    print("Usage: add -t path/to/directory path leads to directory of article xml files")
    print("       add -nlp path/to/directory path leads to directory of article json files")
    exit()


def nlp_approach(input):
    if input:
       dir_name = input
       Run_NLP.launch("", dir_name)
    else:
        sentence = "Durability is an important performance metric of concrete. Freeze-thaw durability is the most important type of \
                    durability of concrete. Freeze-thaw durability has a big impact on concrete strength. This freeze-thaw durability \
                    is largely affected by the small air voids in concrete. These small air voids can release the internal stress in their \
                    surroundings. As a result, the stress build-up in concrete is reduced. These small air voids are usually intentionally \
                    entrained into the concrete during fabrication. The diameter of these small air voids is less than 200 um."
        Run_NLP.launch(sentence, "")

def table_approach(directory):
    mypath = directory
    onlyfiles = [join(mypath,f) for f in listdir(mypath) if isfile(join(mypath, f))]
    print("processing tables from:", onlyfiles)

    process_table_data.process_tables(onlyfiles)




def main():
    args = sys.argv
    if len(args) == 1:
        err_msg()
    flag = args[1]
    if flag == "-nlp":
        try:
            nlp_approach(args[2])   #run nlp on full articles with path specified input
        except:
            nlp_approach("")     #run on hardcoded sentence
    elif flag == "-t":
        try:
            table_approach(args[2])
        except:
            err_msg()
    else:
        err_msg()


if __name__ == '__main__':
    main()
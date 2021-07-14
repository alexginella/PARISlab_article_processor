NOTE: Commands given are for the ubuntu subsystem on windows (download ubuntu in microsoft store)

1) 	create a new python virtual environment:
	python -m venv ENVIRONMENT_NAME

2) 	activate said environment:
	source ENVIRONMENT_NAME/bin/activate

3)	install dependencies:
	pip install -r requirements.txt

4)	download spacy english model
	python -m spacy download en_core_web_sm

5)
	Usage: 
	add -t path/to/directory path leads to directory of article xml files
       	add -nlp path/to/directory path leads to directory of article json files

	ex: python run_pipeline.py -nlp ./json-files

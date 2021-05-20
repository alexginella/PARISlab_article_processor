import requests

piis = ["S0008884619311421", "S0950061820301434", "S0008884619316515", "S0958946514001863", "S0958946516302517", "S0008884611002274", "S0950061819316277"]
#urls = ["https://api.elsevier.com/content/article/pii/S0008884619311421?view=FULL"]

def get_xml(piis):
	for i, pii in enumerate(piis):
		url = "https://api.elsevier.com/content/article/pii/" + pii + "?view=FULL"

		headers = {
			'Accept': 'application/json',
			'X-ELS-APIKey': 'd1b3fde6f5ea01a875dc30d66aa57da1',
			'X-ELS-Insttoken': '25408774f80ee26036234512bef4723b'
		}

		params = {
			"httpAccept:" "application/json"
		}

		r = requests.get(url, headers=headers)
		print("status:", r.status_code)

		writefile = open('json-files/article{}.json'.format(i), 'wb')
		if r.status_code == 200:
			for chunk in r.iter_content(2048):
				writefile.write(chunk)
			writefile.close()

get_xml(piis)
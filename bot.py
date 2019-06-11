import requests

URL = "https://localhost:44326/api/postNews"

data = {
	"title":"Naslov test članka poslanog kroz API, koristeći python skriptu",
	"text":"Tekst test članka poslanog kroz API, koristeći python skriptu. Hvala API, veoma kul. ",
	"image":"https://via.placeholder.com/350x150"
}

requests.post(URL, json=data, verify=False)
import requests
import json
from flask import Flask, render_template, request

app = Flask(__name__)

url_base = "http://ws.audioscrobbler.com/2.0/"
api_key = "c4831afa75cd37744a4a125684dcc64d"

@app.route('/')
def inicio():
    return render_template("inicio.html")

@app.route('/buscador', methods=['GET', 'POST'])
def buscar():
    if request.method == 'POST':
        artista = request.form.get('artista')

        if not artista:
            return render_template('error.html', message="No se proporcionó un nombre de artista válido.")

        payload_bio = {
            "method": "artist.getinfo",
            "artist": artista,
            "api_key": api_key,
            "format": "json"
        }

        response_bio = requests.get(url_base, params=payload_bio)

        if response_bio.status_code == 200:
            data_bio = json.loads(response_bio.text)
            if "error" in data_bio:
                return render_template('error.html', message=data_bio["message"])
            else:
                bio = data_bio["artist"]["bio"]["content"]

                payload_top = {
                    "method": "artist.gettoptracks",
                    "artist": artista,
                    "api_key": api_key,
                    "format": "json",
                    "limit": 5
                }

                response_top5 = requests.get(url_base, params=payload_top)

                if response_top5.status_code == 200:
                    data_top = json.loads(response_top5.text)
                    if "error" in data_top:
                        return render_template('error.html', message=data_top["message"])
                    else:
                        top_tracks = data_top["toptracks"]["track"]
                        return render_template('info.html', artista=artista, bio=bio, top_tracks=top_tracks)
                else:
                    return render_template('error.html', message="Ha ocurrido un error al obtener el top de canciones.")
        else:
            return render_template('error.html', message="Ha ocurrido un error al realizar la petición de la biografía.")
    else:
        return render_template("buscador.html")

if __name__ == '__main__':
    app.run("0.0.0.0", 5000, debug=True)

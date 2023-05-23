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
        query = request.form.get('query')
        tipo = request.form.get('tipo')

        if not query:
            return render_template('error.html', message="No se proporcionó un término de búsqueda válido.")

        if tipo == "artista":
            parametros_bio = {
                "method": "artist.getinfo",
                "artist": query,
                "api_key": api_key,
                "format": "json"
            }

            response_bio = requests.get(url_base, params=parametros_bio)

            if response_bio.status_code == 200:
                data_bio = json.loads(response_bio.text)
                if "error" in data_bio:
                    return render_template('error.html', message=data_bio["message"])
                else:
                    bio = data_bio["artist"]["bio"]["content"]

                    parametros_top = {
                        "method": "artist.gettoptracks",
                        "artist": query,
                        "api_key": api_key,
                        "format": "json",
                        "limit": 5
                    }

                    response_top5 = requests.get(url_base, params=parametros_top)

                    if response_top5.status_code == 200:
                        data_top = json.loads(response_top5.text)
                        if "error" in data_top:
                            return render_template('error.html', message=data_top["message"])
                        else:
                            top_tracks = data_top["toptracks"]["track"]
                            return render_template('info.html', artista=query, bio=bio, top_tracks=top_tracks)
                    else:
                        return render_template('error.html', message="Ha ocurrido un error al obtener el top de canciones.")
            else:
                return render_template('error.html', message="Ha ocurrido un error al realizar la petición de la biografía.")
        elif tipo == "album":
            parametros_album = {
                "method": "album.getinfo",
                "artist": query,
                "album": query,
                "api_key": api_key,
                "format": "json"
            }

            response_album = requests.get(url_base, params=parametros_album)

            if response_album.status_code == 200:
                data_album = json.loads(response_album.text)
                if "error" in data_album:
                    return render_template('error.html', message=data_album["message"])
                else:
                    album = data_album["album"]["name"]
                    tracks = data_album["album"]["tracks"]["track"]
                    return render_template('album.html', album=album, tracks=tracks)
            else:
                return render_template('error.html', message="Ha ocurrido un error al realizar la petición del álbum.")
        else:
            return render_template('error.html', message="Opción de búsqueda inválida.")
    else:
        return render_template("buscador.html")
    
@app.route('/todo')
def todo():
    parametros = {
        "method": "chart.gettopartists",
        "api_key": api_key,
        "format": "json"
    }

    response = requests.get(url_base, params=parametros)

    if response.status_code == 200:
        data = json.loads(response.text)
        if "error" in data:
            return render_template('error.html', message=data["message"])
        else:
            artists = data["artists"]["artist"]
            return render_template('todo.html', artists=artists)
    else:
        return render_template('error.html', message="Ha ocurrido un error al obtener la lista de artistas.")

@app.route('/artista/<nombre>')
def obtener_artista(nombre):
    parametros_bio = {
        "method": "artist.getinfo",
        "artist": nombre,
        "api_key": api_key,
        "format": "json"
    }
    response_bio = requests.get(url_base, params=parametros_bio)
    if response_bio.status_code == 200:
        data_bio = json.loads(response_bio.text)
        if "error" in data_bio:
            return render_template('error.html', message=data_bio["message"])
        else:
            bio = data_bio["artist"]["bio"]["content"]
            parametros_top = {
                "method": "artist.gettoptracks",
                "artist": nombre,
                "api_key": api_key,
                "format": "json",
                "limit": 5
            }
            response_top5 = requests.get(url_base, params=parametros_top)
            if response_top5.status_code == 200:
                data_top = json.loads(response_top5.text)
                if "error" in data_top:
                    return render_template('error.html', message=data_top["message"])
                else:
                    top_tracks = data_top["toptracks"]["track"]
                    return render_template('info.html', artista=nombre, bio=bio, top_tracks=top_tracks)
            else:
                return render_template('error.html', message="Ha ocurrido un error al obtener el top de canciones.")
    else:
        return render_template('error.html', message="Ha ocurrido un error al realizar la petición de la biografía.")


app.run("0.0.0.0", 5000, debug=True)

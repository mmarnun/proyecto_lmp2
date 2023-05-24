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
            return render_template('error.html', mensaje="No se proporcionó un término de búsqueda válido.")

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
                if "artist" in data_bio:
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
                        top_tracks = data_top["toptracks"]["track"]
                        return render_template('info.html', artista=query, bio=bio, top_tracks=top_tracks)
                return render_template('error.html', mensaje="No se encontró ningún resultado.")
            else:
                return render_template('error.html', mensaje="No se encontró ningún resultado.")
        elif tipo == "tag":
            parametros_tag = {
                "method": "tag.getinfo",
                "tag": query,
                "api_key": api_key,
                "format": "json"
            }
            response_tag = requests.get(url_base, params=parametros_tag)
            if response_tag.status_code == 200:
                data_tag = json.loads(response_tag.text)
                tag_info = data_tag["tag"]
                return render_template('tag.html', tag_info=tag_info)
            else:
                return render_template('error.html', mensaje="No se encontró ningún resultado.")
        elif tipo == "cadena":
            parametros_top50 = {
                "method": "chart.gettopartists",
                "api_key": api_key,
                "format": "json",
            }
            response_top50 = requests.get(url_base, params=parametros_top50)
            if response_top50.status_code == 200:
                data_top50 = json.loads(response_top50.text)
                artists = data_top50["artists"]["artist"]
                filtro = [artist for artist in artists if query.lower() in artist["name"].lower()]
                if filtro:
                    return render_template('todo.html', artists=filtro)
                else:
                    return render_template('error.html', mensaje="No se encontró ningún resultado.")
        else:
            return render_template('error.html', mensaje="Opción de búsqueda inválida.")
    else:
        return render_template("buscador.html")

@app.route('/todo')
def todo():
    parametros = {
        "method": "chart.gettopartists",
        "api_key": api_key,
        "format": "json",
    }
    response = requests.get(url_base, params=parametros)
    if response.status_code == 200:
        data = json.loads(response.text)
        if "error" in data:
            return render_template('error.html', mensaje=data["mensaje"])
        else:
            artists = data["artists"]["artist"]
            return render_template('todo.html', artists=artists)

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
            top_tracks = data_top["toptracks"]["track"]
            return render_template('info.html', artista=nombre, bio=bio, top_tracks=top_tracks)

app.run("0.0.0.0", 5000, debug=True)

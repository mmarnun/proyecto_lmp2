from flask import Flask, render_template, request, redirect, url_for, abort

app = Flask(__name__)

@app.route('/inicio')
def inicio():
    return render_template("inicio.html")

@app.route('/buscador')
def buscador():
    # Lógica para el buscador
    return render_template("buscador.html")

@app.route('/todo')
def todo():
    # Lógica para la página "Todo"
    return render_template("todo.html")

if __name__ == '__main__':
    app.run("0.0.0.0", 5000, debug=True)

from flask import Flask, render_template, request, redirect, url_for
import pyrebase
import base64

app = Flask(__name__)
config = {
    "apiKey": "AIzaSyBIgHJuuVFKvqY6FaHITWpwy6ImKpsBEMA",
    "authDomain": "olimpiadas-champagnat.firebaseapp.com",
    "projectId": "olimpiadas-champagnat",
    "storageBucket": "olimpiadas-champagnat.appspot.com",
    "messagingSenderId": "521824711033",
    "appId": "1:521824711033:web:ce71b3e7600d79e6297fa8",
    "serviceAccount": "serviceAccount.json",
    "databaseURL": "https://olimpiadas-champagnat-default-rtdb.firebaseio.com/"
}
# config para o firebase
firebase = pyrebase.initialize_app(config)
bd = firebase.database()


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]

        dados_usuario_bd = bd.child(f"usuarios/{usuario}").get().val()

        # verifica se o usuario existe e se a senha fornecida é valida
        if dados_usuario_bd and dados_usuario_bd['senha'] == senha:
            return redirect(url_for("index"))

        else:
            return render_template("login.html", erro="Usuário ou senha inválido.")

    return render_template("login.html", erro="")


@app.route("/configurações", methods=["GET", "POST"])
def configuracoes():
    if request.method == "POST":
        imagem = request.files["imagem"]
        imagem_b64 = base64.b64encode(imagem.read()).decode("utf-8")
        bd.child("usuarios/usuario0").set({"foto_de_perfil": imagem_b64})

    return render_template("configuracoes.html")


if __name__ == '__main__':
    app.run(debug=True)


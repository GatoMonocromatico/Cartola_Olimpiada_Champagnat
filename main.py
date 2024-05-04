import re
from flask import Flask, render_template, request, redirect, url_for
import pyrebase
import base64
import io
from PIL import Image
from flask_login import current_user, UserMixin, login_user, LoginManager, login_required
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('CHAVE_SECRETA_FLASK')
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, dados, eh_novo):
        self.id = dados["id"]
        self.nome = dados["nome"]
        self.senha = dados["senha"]
        if eh_novo:
            self.foto_de_perfil = ""
            self.esportes_cadastrados = ""
            bd.child(f"usuarios/{self.id}").set({
                "esportes_cadastrados": "", "foto_de_perfil": "", "nome": self.nome, "senha": self.senha, "id": self.id
            })
        else:
            self.foto_de_perfil = dados["foto_de_perfil"]
            self.esportes_cadastrados = dados["esportes_cadastrados"]


config = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": os.getenv("FIREBASE_APP_ID"),
    "serviceAccount": "serviceAccount.json",
    "databaseURL": os.getenv("FIREBASE_DATABASE_URL")
}
# config para o firebase
firebase = pyrebase.initialize_app(config)
bd = firebase.database()


@login_manager.user_loader
def carrega_usuario(user_id):
    dados_usuario = bd.child(f"usuarios/{user_id}").get().val()
    if dados_usuario:
        return User(dados_usuario, False)
    else:
        return None

@app.route("/", methods=["GET"])
def index():

    # transforma o código em base64 fornecido em bytes para png garantindo que todos os dados serão PNG

    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]

        if "signup" in request.form and not bd.child(f"usuarios/{usuario}").get().val():

            nome = request.form["nome"]
            lista_partes_nome = nome.split(" ")

            padrao_nome = re.compile(r"[A-Z][a-z]+")  # padrão (nome começa com letra maiúscula)
            lista_excecoes = ("de", "da", "do", "dos", "das")  # partes de um nome que podem não começar com letra maiúscula

            index_for = 0
            for parte_nome in lista_partes_nome:
                if not re.fullmatch(padrao_nome, parte_nome):  # se a parte do nome não atende o padrão
                    if parte_nome not in lista_excecoes:
                        return render_template("login.html", erro="Nome inválido")  # ela não pode não estar na lista de exceções
                    elif index_for == 0:
                        return render_template("login.html", erro="Nome inválido")  # nenhum nome começa com preposição
                index_for += 1

            nome = ""
            index_for = 0
            for nome_parte in lista_partes_nome:
                if index_for > 0:
                    nome += f" {nome_parte}"
                else:
                    nome += nome_parte
                index_for += 1

            padrao_usuario = re.compile(r"\d\d\d\d\d\d\d\d")

            if not re.fullmatch(padrao_usuario, usuario):
                return render_template("login.html", erro="Número de matrícula inválido")

            user = User({
                "nome": nome,
                "senha": senha,
                "id": usuario
                }, True)
            login_user(user)  # loga usuario
            return redirect(url_for("index"))
        else:
            dados = bd.child(f"usuarios/{usuario}").get().val()

            if not dados:
                return render_template("login.html", erro="Usuário inexistente")
            elif dados["senha"] != senha:
                return render_template("login.html", erro="Senha inválida")
            else:
                user = User(dados, False)
                login_user(user)
                return redirect(url_for("index"))
    return render_template("login.html", erro="")


@app.route("/configurações", methods=["GET", "POST"])
@login_required
def configuracoes():
    if request.method == "POST":
        imagem_bytes = request.files["imagem"].read()
        buffer = io.BytesIO(imagem_bytes)
        imagem = Image.open(buffer)
        buffer_png = io.BytesIO()
        imagem.save(buffer_png, format="PNG")
        bytes_png = buffer_png.getvalue()
        imagem_b64_png = base64.b64encode(bytes_png).decode("utf-8")
        bd.child(f"usuarios/{current_user.id}").update({"foto_de_perfil": imagem_b64_png})
        current_user.foto_de_perfil = imagem_b64_png

    foto_de_perfil = current_user.foto_de_perfil
    id = current_user.id
    nome = current_user.nome

    return render_template("configuracoes.html", nome_e_matricula=f"{id} {nome}", imagem_b64=foto_de_perfil)


if __name__ == '__main__':
    app.run(debug=True)


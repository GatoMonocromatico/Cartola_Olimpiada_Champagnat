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
            self.foto_de_perfil = "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"
            self.esportes_cadastrados = ""
            bd.child(f"usuarios/{self.id}").set({
                "esportes_cadastrados": "", "foto_de_perfil": self.foto_de_perfil, "nome": self.nome, "senha": self.senha, "id": self.id
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
    nome = ""
    foto_de_perfil = ""
    if current_user.is_authenticated:
        nome = current_user.nome
        foto_de_perfil = current_user.foto_de_perfil

    return render_template("index.html", nome_de_usuario=nome, foto_de_perfil=foto_de_perfil)


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
        # com a imagem iniciada na biblioteca pillow vou recorta-la para formar um quadrado perfeito, caso não seja
        largura, altura = imagem.size
        if altura != largura:
            if largura > altura:
                quantidade_cortar_cada = int((largura - altura)/2)
                recorte_coordenadas = (quantidade_cortar_cada, 0, int(largura-quantidade_cortar_cada), altura)
            else:
                quantidade_cortar_cada = int((altura - largura)/2)
                recorte_coordenadas = (0, quantidade_cortar_cada, largura, int(altura-quantidade_cortar_cada))

            imagem_formatada = imagem.crop(recorte_coordenadas)
        else:
            imagem_formatada = imagem

        buffer_png = io.BytesIO()
        imagem_formatada.save(buffer_png, format="PNG")
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


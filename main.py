import re
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import pyrebase
import base64
import io
from PIL import Image
from flask_login import current_user, UserMixin, login_user, LoginManager, login_required
import os
from dotenv import load_dotenv
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, BooleanField
from wtforms.validators import data_required, Length
import smtplib
import email.message
import secrets
import string


load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('CHAVE_SECRETA_FLASK')

csrf = CSRFProtect(app)

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
storage = firebase.storage()


class ADMAutorizarForm(FlaskForm):
    code = StringField("Código", validators=[Length(min=6, max=6)])
    submit = SubmitField("Enviar")


class ADMForm(FlaskForm):
    alterar_mercado_futsalM = SubmitField("Trocar")
    alterar_mercado_futsalF = SubmitField("Trocar")
    alterar_mercado_basquete = SubmitField("Trocar")
    alterar_mercado_handebol = SubmitField("Trocar")

    futsalM = SubmitField("Pontuar Futsal Masculino")
    futsalF = SubmitField("Pontuar Futsal Feminino")
    basquete = SubmitField("Pontuar Basquete")
    handebol = SubmitField("Pontuar Handebol")


class InserirPontuacaoFormFutsalM(FlaskForm):
    nome_esporte = StringField("esporte", default="futsal_masculino")

    jogadores_raw = bd.child("jogadores/futsal_masculino").get().val()
    jogadores_ataque = {}
    jogadores_gol = {}
    for posicao in jogadores_raw:
        if posicao == "ataque":
            jogadores_ataque = jogadores_raw[posicao]
        else:
            jogadores_gol = jogadores_raw[posicao]

    escolhas_goleiro = [("", "-Escolha um jogador se preciso-")]
    for jogador in jogadores_gol:
        tupla_escolha = (jogador, f"{jogadores_gol[jogador]['nome']} - {jogadores_gol[jogador]['equipe']} ({jogador})")
        escolhas_goleiro.append(tupla_escolha)

    escolhas_ataque = [("", "-Escolha um jogador se preciso-")]
    for jogador in jogadores_ataque:
        tupla_escolha = (jogador, f"{jogadores_ataque[jogador]['nome']} - {jogadores_ataque[jogador]['equipe']} ({jogador})")
        escolhas_ataque.append(tupla_escolha)

    gols_goleiro1 = IntegerField("Gols", default=0)
    gols_goleiro2 = IntegerField("Gols", default=0)
    defesas_goleiro1 = IntegerField("Defesas", default=0)
    defesas_goleiro2 = IntegerField("Defesas", default=0)
    amarelos_goleiro1 = IntegerField("Cartões amarelos", default=0)
    amarelos_goleiro2 = IntegerField("Cartões amarelos", default=0)
    vermelho_goleiro1 = BooleanField("Cartão vermelho")
    vermelho_goleiro2 = BooleanField("Cartão vermelho")
    faltas_goleiro1 = IntegerField("Faltas", default=0)
    faltas_goleiro2 = IntegerField("Faltas", default=0)
    assistencias_goleiro1 = IntegerField("Assistências", default=0)
    assistencias_goleiro2 = IntegerField("Assistências", default=0)

    goleiro1 = SelectField("Goleiro time 1", choices=escolhas_goleiro)
    goleiro2 = SelectField("Goleiro time 2", choices=escolhas_goleiro)

    jogador1 = SelectField("Jogador1 time 1", choices=escolhas_ataque)
    jogador2 = SelectField("Jogador2 time 1", choices=escolhas_ataque)
    jogador3 = SelectField("Jogador3 time 1", choices=escolhas_ataque)
    jogador4 = SelectField("Jogador4 time 1", choices=escolhas_ataque)
    jogador5 = SelectField("Jogador1 time 2", choices=escolhas_ataque)
    jogador6 = SelectField("Jogador2 time 2", choices=escolhas_ataque)
    jogador7 = SelectField("Jogador3 time 2", choices=escolhas_ataque)
    jogador8 = SelectField("Jogador4 time 2", choices=escolhas_ataque)

    pontos_jogador1 = IntegerField("Gols", default=0)
    pontos_jogador2 = IntegerField("Gols", default=0)
    pontos_jogador3 = IntegerField("Gols", default=0)
    pontos_jogador4 = IntegerField("Gols", default=0)
    pontos_jogador5 = IntegerField("Gols", default=0)
    pontos_jogador6 = IntegerField("Gols", default=0)
    pontos_jogador7 = IntegerField("Gols", default=0)
    pontos_jogador8 = IntegerField("Gols", default=0)

    amarelos_jogador1 = IntegerField("Cartões amarelos", default=0)
    amarelos_jogador2 = IntegerField("Cartões amarelos", default=0)
    amarelos_jogador3 = IntegerField("Cartões amarelos", default=0)
    amarelos_jogador4 = IntegerField("Cartões amarelos", default=0)
    amarelos_jogador5 = IntegerField("Cartões amarelos", default=0)
    amarelos_jogador6 = IntegerField("Cartões amarelos", default=0)
    amarelos_jogador7 = IntegerField("Cartões amarelos", default=0)
    amarelos_jogador8 = IntegerField("Cartões amarelos", default=0)

    vermelho_jogador1 = BooleanField("Cartão vermelho")
    vermelho_jogador2 = BooleanField("Cartão vermelho")
    vermelho_jogador3 = BooleanField("Cartão vermelho")
    vermelho_jogador4 = BooleanField("Cartão vermelho")
    vermelho_jogador5 = BooleanField("Cartão vermelho")
    vermelho_jogador6 = BooleanField("Cartão vermelho")
    vermelho_jogador7 = BooleanField("Cartão vermelho")
    vermelho_jogador8 = BooleanField("Cartão vermelho")

    faltas_jogador1 = IntegerField("Faltas", default=0)
    faltas_jogador2 = IntegerField("Faltas", default=0)
    faltas_jogador3 = IntegerField("Faltas", default=0)
    faltas_jogador4 = IntegerField("Faltas", default=0)
    faltas_jogador5 = IntegerField("Faltas", default=0)
    faltas_jogador6 = IntegerField("Faltas", default=0)
    faltas_jogador7 = IntegerField("Faltas", default=0)
    faltas_jogador8 = IntegerField("Faltas", default=0)

    assistencias_jogador1 = IntegerField("Assistências", default=0)
    assistencias_jogador2 = IntegerField("Assistências", default=0)
    assistencias_jogador3 = IntegerField("Assistências", default=0)
    assistencias_jogador4 = IntegerField("Assistências", default=0)
    assistencias_jogador5 = IntegerField("Assistências", default=0)
    assistencias_jogador6 = IntegerField("Assistências", default=0)
    assistencias_jogador7 = IntegerField("Assistências", default=0)
    assistencias_jogador8 = IntegerField("Assistências", default=0)

    submit = SubmitField("Confirmar")


class InserirPontuacaoFormFutsalF(FlaskForm):
    nome_esporte = StringField("esporte", default="futsal_feminino")

    jogadores_raw = bd.child("jogadores/futsal_feminino").get().val()
    jogadores_ataque = {}
    jogadores_gol = {}
    for posicao in jogadores_raw:
        if posicao == "ataque":
            jogadores_ataque = jogadores_raw[posicao]
        else:
            jogadores_gol = jogadores_raw[posicao]

    escolhas_goleiro = [("", "-Escolha um jogador se preciso-")]
    for jogador in jogadores_gol:
        tupla_escolha = (jogador, f"{jogadores_gol[jogador]['nome']} - {jogadores_gol[jogador]['equipe']} ({jogador})")
        escolhas_goleiro.append(tupla_escolha)

    escolhas_ataque = [("", "-Escolha um jogador se preciso-")]
    for jogador in jogadores_ataque:
        tupla_escolha = (jogador, f"{jogadores_ataque[jogador]['nome']} - {jogadores_ataque[jogador]['equipe']} ({jogador})")
        escolhas_ataque.append(tupla_escolha)

    goleiro1 = SelectField("Goleira time 1", choices=escolhas_goleiro)
    goleiro2 = SelectField("Goleira time 2", choices=escolhas_goleiro)
    gols_goleiro1 = IntegerField("Gols", default=0)
    gols_goleiro2 = IntegerField("Gols", default=0)
    defesas_goleiro1 = IntegerField("Defesas", default=0)
    defesas_goleiro2 = IntegerField("Defesas", default=0)
    amarelos_goleiro1 = IntegerField("Cartões amarelos", default=0)
    amarelos_goleiro2 = IntegerField("Cartões amarelos", default=0)
    vermelho_goleiro1 = BooleanField("Cartão vermelho")
    vermelho_goleiro2 = BooleanField("Cartão vermelho")
    faltas_goleiro1 = IntegerField("Faltas", default=0)
    faltas_goleiro2 = IntegerField("Faltas", default=0)
    assistencias_goleiro1 = IntegerField("Assistências", default=0)
    assistencias_goleiro2 = IntegerField("Assistências", default=0)

    jogador1 = SelectField("Jogadora1 time 1", choices=escolhas_ataque)
    jogador2 = SelectField("Jogadora2 time 1", choices=escolhas_ataque)
    jogador3 = SelectField("Jogadora3 time 1", choices=escolhas_ataque)
    jogador4 = SelectField("Jogadora4 time 1", choices=escolhas_ataque)
    jogador5 = SelectField("Jogadora1 time 2", choices=escolhas_ataque)
    jogador6 = SelectField("Jogadora2 time 2", choices=escolhas_ataque)
    jogador7 = SelectField("Jogadora3 time 2", choices=escolhas_ataque)
    jogador8 = SelectField("Jogadora4 time 2", choices=escolhas_ataque)

    pontos_jogador1 = IntegerField("Gols", default=0)
    pontos_jogador2 = IntegerField("Gols", default=0)
    pontos_jogador3 = IntegerField("Gols", default=0)
    pontos_jogador4 = IntegerField("Gols", default=0)
    pontos_jogador5 = IntegerField("Gols", default=0)
    pontos_jogador6 = IntegerField("Gols", default=0)
    pontos_jogador7 = IntegerField("Gols", default=0)
    pontos_jogador8 = IntegerField("Gols", default=0)

    amarelos_jogador1 = IntegerField("Cartões amarelos", default=0)
    amarelos_jogador2 = IntegerField("Cartões amarelos", default=0)
    amarelos_jogador3 = IntegerField("Cartões amarelos", default=0)
    amarelos_jogador4 = IntegerField("Cartões amarelos", default=0)
    amarelos_jogador5 = IntegerField("Cartões amarelos", default=0)
    amarelos_jogador6 = IntegerField("Cartões amarelos", default=0)
    amarelos_jogador7 = IntegerField("Cartões amarelos", default=0)
    amarelos_jogador8 = IntegerField("Cartões amarelos", default=0)

    vermelho_jogador1 = BooleanField("Cartão vermelho")
    vermelho_jogador2 = BooleanField("Cartão vermelho")
    vermelho_jogador3 = BooleanField("Cartão vermelho")
    vermelho_jogador4 = BooleanField("Cartão vermelho")
    vermelho_jogador5 = BooleanField("Cartão vermelho")
    vermelho_jogador6 = BooleanField("Cartão vermelho")
    vermelho_jogador7 = BooleanField("Cartão vermelho")
    vermelho_jogador8 = BooleanField("Cartão vermelho")

    faltas_jogador1 = IntegerField("Faltas", default=0)
    faltas_jogador2 = IntegerField("Faltas", default=0)
    faltas_jogador3 = IntegerField("Faltas", default=0)
    faltas_jogador4 = IntegerField("Faltas", default=0)
    faltas_jogador5 = IntegerField("Faltas", default=0)
    faltas_jogador6 = IntegerField("Faltas", default=0)
    faltas_jogador7 = IntegerField("Faltas", default=0)
    faltas_jogador8 = IntegerField("Faltas", default=0)

    assistencias_jogador1 = IntegerField("Assistências", default=0)
    assistencias_jogador2 = IntegerField("Assistências", default=0)
    assistencias_jogador3 = IntegerField("Assistências", default=0)
    assistencias_jogador4 = IntegerField("Assistências", default=0)
    assistencias_jogador5 = IntegerField("Assistências", default=0)
    assistencias_jogador6 = IntegerField("Assistências", default=0)
    assistencias_jogador7 = IntegerField("Assistências", default=0)
    assistencias_jogador8 = IntegerField("Assistências", default=0)

    submit = SubmitField("Confirmar")


class InserirPontuacaoFormBasquete(FlaskForm):
    nome_esporte = StringField("esporte", default="basquete")

    jogadores = bd.child("jogadores/basquete/ataque").get().val()

    escolhas = [("", "-Escolha um jogador se preciso-")]
    for jogador in jogadores:
        tupla_escolha = (jogador, f"{jogadores[jogador]['nome']} - {jogadores[jogador]['equipe']} ({jogador})")
        escolhas.append(tupla_escolha)

    jogador1 = SelectField("Jogador1 time 1", choices=escolhas)
    jogador2 = SelectField("Jogador2 time 1", choices=escolhas)
    jogador3 = SelectField("Jogador3 time 1", choices=escolhas)
    jogador4 = SelectField("Jogador4 time 1", choices=escolhas)
    jogador5 = SelectField("Jogador5 time 1", choices=escolhas)
    jogador6 = SelectField("Jogador1 time 2", choices=escolhas)
    jogador7 = SelectField("Jogador2 time 2", choices=escolhas)
    jogador8 = SelectField("Jogador3 time 2", choices=escolhas)
    jogador9 = SelectField("Jogador4 time 2", choices=escolhas)
    jogador10 = SelectField("Jogador5 time 2", choices=escolhas)

    pontos_jogador1 = IntegerField("Pontos", default=0)
    pontos_jogador2 = IntegerField("Pontos", default=0)
    pontos_jogador3 = IntegerField("Pontos", default=0)
    pontos_jogador4 = IntegerField("Pontos", default=0)
    pontos_jogador5 = IntegerField("Pontos", default=0)
    pontos_jogador6 = IntegerField("Pontos", default=0)
    pontos_jogador7 = IntegerField("Pontos", default=0)
    pontos_jogador8 = IntegerField("Pontos", default=0)
    pontos_jogador9 = IntegerField("Pontos", default=0)
    pontos_jogador10 = IntegerField("Pontos", default=0)

    amarelos_jogador1 = IntegerField("Cartões amarelos", default=0)
    amarelos_jogador2 = IntegerField("Cartões amarelos", default=0)
    amarelos_jogador3 = IntegerField("Cartões amarelos", default=0)
    amarelos_jogador4 = IntegerField("Cartões amarelos", default=0)
    amarelos_jogador5 = IntegerField("Cartões amarelos", default=0)
    amarelos_jogador6 = IntegerField("Cartões amarelos", default=0)
    amarelos_jogador7 = IntegerField("Cartões amarelos", default=0)
    amarelos_jogador8 = IntegerField("Cartões amarelos", default=0)
    amarelos_jogador9 = IntegerField("Cartões amarelos", default=0)
    amarelos_jogador10 = IntegerField("Cartões amarelos", default=0)


    vermelho_jogador1 = BooleanField("Cartão vermelho")
    vermelho_jogador2 = BooleanField("Cartão vermelho")
    vermelho_jogador3 = BooleanField("Cartão vermelho")
    vermelho_jogador4 = BooleanField("Cartão vermelho")
    vermelho_jogador5 = BooleanField("Cartão vermelho")
    vermelho_jogador6 = BooleanField("Cartão vermelho")
    vermelho_jogador7 = BooleanField("Cartão vermelho")
    vermelho_jogador8 = BooleanField("Cartão vermelho")
    vermelho_jogador9 = BooleanField("Cartão vermelho")
    vermelho_jogador10 = BooleanField("Cartão vermelho")

    faltas_jogador1 = IntegerField("Faltas", default=0)
    faltas_jogador2 = IntegerField("Faltas", default=0)
    faltas_jogador3 = IntegerField("Faltas", default=0)
    faltas_jogador4 = IntegerField("Faltas", default=0)
    faltas_jogador5 = IntegerField("Faltas", default=0)
    faltas_jogador6 = IntegerField("Faltas", default=0)
    faltas_jogador7 = IntegerField("Faltas", default=0)
    faltas_jogador8 = IntegerField("Faltas", default=0)
    faltas_jogador9 = IntegerField("Faltas", default=0)
    faltas_jogador10 = IntegerField("Faltas", default=0)

    assistencias_jogador1 = IntegerField("Assistências", default=0)
    assistencias_jogador2 = IntegerField("Assistências", default=0)
    assistencias_jogador3 = IntegerField("Assistências", default=0)
    assistencias_jogador4 = IntegerField("Assistências", default=0)
    assistencias_jogador5 = IntegerField("Assistências", default=0)
    assistencias_jogador6 = IntegerField("Assistências", default=0)
    assistencias_jogador7 = IntegerField("Assistências", default=0)
    assistencias_jogador8 = IntegerField("Assistências", default=0)
    assistencias_jogador9 = IntegerField("Assistências", default=0)
    assistencias_jogador10 = IntegerField("Assistências", default=0)

    submit = SubmitField("Confirmar")


class InserirPontuacaoFormHandebol(FlaskForm):
    nome_esporte = StringField("esporte", default="handebol")

    jogadores_raw = bd.child("jogadores/handebol").get().val()
    jogadores_ataque = {}
    jogadores_gol = {}
    for posicao in jogadores_raw:
        if posicao == "ataque":
            jogadores_ataque = jogadores_raw[posicao]
        else:
            jogadores_gol = jogadores_raw[posicao]

    escolhas_goleiro = [("", "-Escolha um jogador se preciso-")]
    for jogador in jogadores_gol:
        tupla_escolha = (jogador, f"{jogadores_gol[jogador]['nome']} - {jogadores_gol[jogador]['equipe']} ({jogador})")
        escolhas_goleiro.append(tupla_escolha)

    escolhas_ataque = [("", "-Escolha um jogador se preciso-")]
    for jogador in jogadores_ataque:
        tupla_escolha = (jogador, f"{jogadores_ataque[jogador]['nome']} - {jogadores_ataque[jogador]['equipe']} ({jogador})")
        escolhas_ataque.append(tupla_escolha)

    goleiro1 = SelectField("Goleira time 1", choices=escolhas_goleiro)
    goleiro2 = SelectField("Goleira time 2", choices=escolhas_goleiro)
    gols_goleiro1 = IntegerField("Gols", default=0)
    gols_goleiro2 = IntegerField("Gols", default=0)
    defesas_goleiro1 = IntegerField("Defesas", default=0)
    defesas_goleiro2 = IntegerField("Defesas", default=0)
    amarelos_goleiro1 = IntegerField("Cartões amarelos", default=0)
    amarelos_goleiro2 = IntegerField("Cartões amarelos", default=0)
    vermelho_goleiro1 = BooleanField("Cartão vermelho")
    vermelho_goleiro2 = BooleanField("Cartão vermelho")
    faltas_goleiro1 = IntegerField("Faltas", default=0)
    faltas_goleiro2 = IntegerField("Faltas", default=0)
    assistencias_goleiro1 = IntegerField("Assistências", default=0)
    assistencias_goleiro2 = IntegerField("Assistências", default=0)

    jogador1 = SelectField("Jogadora1 time 1", choices=escolhas_ataque)
    jogador2 = SelectField("Jogadora2 time 1", choices=escolhas_ataque)
    jogador3 = SelectField("Jogadora3 time 1", choices=escolhas_ataque)
    jogador4 = SelectField("Jogadora4 time 1", choices=escolhas_ataque)
    jogador5 = SelectField("Jogadora5 time 1", choices=escolhas_ataque)
    jogador6 = SelectField("Jogadora6 time 1", choices=escolhas_ataque)
    jogador7 = SelectField("Jogadora1 time 2", choices=escolhas_ataque)
    jogador8 = SelectField("Jogadora2 time 2", choices=escolhas_ataque)
    jogador9 = SelectField("Jogadora3 time 2", choices=escolhas_ataque)
    jogador10 = SelectField("Jogadora4 time 2", choices=escolhas_ataque)
    jogador11 = SelectField("Jogadora5 time 2", choices=escolhas_ataque)
    jogador12 = SelectField("Jogadora6 time 2", choices=escolhas_ataque)

    pontos_jogador1 = IntegerField("Gols", default=0)
    pontos_jogador2 = IntegerField("Gols", default=0)
    pontos_jogador3 = IntegerField("Gols", default=0)
    pontos_jogador4 = IntegerField("Gols", default=0)
    pontos_jogador5 = IntegerField("Gols", default=0)
    pontos_jogador6 = IntegerField("Gols", default=0)
    pontos_jogador7 = IntegerField("Gols", default=0)
    pontos_jogador8 = IntegerField("Gols", default=0)
    pontos_jogador9 = IntegerField("Gols", default=0)
    pontos_jogador10 = IntegerField("Gols", default=0)
    pontos_jogador11 = IntegerField("Gols", default=0)
    pontos_jogador12 = IntegerField("Gols", default=0)

    amarelos_jogador1 = IntegerField("Cartões amarelos", default=0)
    amarelos_jogador2 = IntegerField("Cartões amarelos", default=0)
    amarelos_jogador3 = IntegerField("Cartões amarelos", default=0)
    amarelos_jogador4 = IntegerField("Cartões amarelos", default=0)
    amarelos_jogador5 = IntegerField("Cartões amarelos", default=0)
    amarelos_jogador6 = IntegerField("Cartões amarelos", default=0)
    amarelos_jogador7 = IntegerField("Cartões amarelos", default=0)
    amarelos_jogador8 = IntegerField("Cartões amarelos", default=0)
    amarelos_jogador9 = IntegerField("Cartões amarelos", default=0)
    amarelos_jogador10 = IntegerField("Cartões amarelos", default=0)
    amarelos_jogador11 = IntegerField("Cartões amarelos", default=0)
    amarelos_jogador12 = IntegerField("Cartões amarelos", default=0)

    vermelho_jogador1 = BooleanField("Cartão vermelho")
    vermelho_jogador2 = BooleanField("Cartão vermelho")
    vermelho_jogador3 = BooleanField("Cartão vermelho")
    vermelho_jogador4 = BooleanField("Cartão vermelho")
    vermelho_jogador5 = BooleanField("Cartão vermelho")
    vermelho_jogador6 = BooleanField("Cartão vermelho")
    vermelho_jogador7 = BooleanField("Cartão vermelho")
    vermelho_jogador8 = BooleanField("Cartão vermelho")
    vermelho_jogador9 = BooleanField("Cartões vermelhos")
    vermelho_jogador10 = BooleanField("Cartões vermelhos")
    vermelho_jogador11 = BooleanField("Cartões vermelhos")
    vermelho_jogador12 = BooleanField("Cartões vermelhos")

    faltas_jogador1 = IntegerField("Faltas", default=0)
    faltas_jogador2 = IntegerField("Faltas", default=0)
    faltas_jogador3 = IntegerField("Faltas", default=0)
    faltas_jogador4 = IntegerField("Faltas", default=0)
    faltas_jogador5 = IntegerField("Faltas", default=0)
    faltas_jogador6 = IntegerField("Faltas", default=0)
    faltas_jogador7 = IntegerField("Faltas", default=0)
    faltas_jogador8 = IntegerField("Faltas", default=0)
    faltas_jogador9 = IntegerField("faltas", default=0)
    faltas_jogador10 = IntegerField("faltas", default=0)
    faltas_jogador11 = IntegerField("faltas", default=0)
    faltas_jogador12 = IntegerField("faltas", default=0)

    assistencias_jogador1 = IntegerField("Assistências", default=0)
    assistencias_jogador2 = IntegerField("Assistências", default=0)
    assistencias_jogador3 = IntegerField("Assistências", default=0)
    assistencias_jogador4 = IntegerField("Assistências", default=0)
    assistencias_jogador5 = IntegerField("Assistências", default=0)
    assistencias_jogador6 = IntegerField("Assistências", default=0)
    assistencias_jogador7 = IntegerField("Assistências", default=0)
    assistencias_jogador8 = IntegerField("Assistências", default=0)
    assistencias_jogador9 = IntegerField("Assistências", default=0)
    assistencias_jogador10 = IntegerField("Assistências", default=0)
    assistencias_jogador11 = IntegerField("Assistências", default=0)
    assistencias_jogador12 = IntegerField("Assistências", default=0)

    submit = SubmitField("Confirmar")


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(UserMixin):
    def __init__(self, dados, eh_novo):
        self.id = dados["id"]
        self.nome = dados["nome"]
        self.senha = dados["senha"]
        self.equipe = dados["equipe"]
        if eh_novo:
            self.foto_de_perfil = "https://firebasestorage.googleapis.com/v0/b/cartola-olimpiadas-champagnat.appspot.com/o/fotos_de_perfil%2Fusuario_sem_foto.png?alt=media&token=29fa5414-76c1-49ca-b0f4-e0de89d3492d"
            self.esportes_cadastrados = ""
            self.tem_foto_de_perfil_default = True
            self.escalacao = {"basquete": {"jogador1": "", "jogador2": "", "jogador3": "", "jogador4": "", "jogador5": ""},
                              "handebol": {"goleiro": "", "jogador1": "", "jogador2": "", "jogador3": "", "jogador4": "", "jogador5": "", "jogador6": ""},
                              "futsal_feminino": {"goleiro": "", "jogador1": "", "jogador2": "", "jogador3": "", "jogador4": ""},
                              "futsal_masculino": {"goleiro": "", "jogador1": "", "jogador2": "", "jogador3": "", "jogador4": ""}}
            self.pontos = {"futsal_masculino": 0, "futsal_feminino": 0, "basquete": 0, "handebol": 0}
            self.posicao = ""
            self.ADM = False

            bd.child(f"usuarios/{self.id}").set({
                "esportes_cadastrados": "",
                "foto_de_perfil": self.foto_de_perfil,
                "nome": self.nome,
                "senha": self.senha,
                "id": self.id,
                "tem_foto_de_perfil_default": self.tem_foto_de_perfil_default,
                "equipe": self.equipe,
                "escalacao": self.escalacao,
                "pontos": self.pontos,
                "posicao": self.posicao,
                "ADM": self.ADM
            })
        else:
            self.tem_foto_de_perfil_default = dados["tem_foto_de_perfil_default"]
            self.foto_de_perfil = dados["foto_de_perfil"]
            self.esportes_cadastrados = dados["esportes_cadastrados"]
            self.escalacao = dados["escalacao"]
            self.pontos = dados["pontos"]
            self.posicao = dados["posicao"]
            self.ADM = dados["ADM"]


@login_manager.user_loader
def carrega_usuario(user_id):
    dados_usuario = bd.child(f"usuarios/{user_id}").get().val()
    if dados_usuario:
        return User(dados_usuario, False)
    else:
        return None


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    mercado_aberto = bd.child("mercado_aberto").get().val()

    if request.method == "POST":
        dados_raw = request.get_json()

        esporte = dados_raw['1']
        if mercado_aberto[esporte]:
            dados_raw_escalacao = dados_raw['0'].split(";")

            dados_format = []
            for string in dados_raw_escalacao:
                par_info = string.split(",")
                dados_format.append(par_info)

            dict_dados = {}
            for jogador, posicao in dados_format:
                dict_dados[posicao] = jogador

            bd.child(f"usuarios/{current_user.id}/escalacao/{esporte}").update(dict_dados)
            return "escalacao salva com sucesso"
        else:
            return "mercado fechado", 400

    return render_template("index.html", nome_de_usuario=current_user.nome, foto_de_perfil=current_user.foto_de_perfil, mercado_aberto=mercado_aberto, ADM=current_user.ADM)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        dados = request.form

        usuario = dados["usuario"]
        senha = dados["senha"]

        if "signup" in dados:
            if not bd.child(f"usuarios/{usuario}").get().val():
                equipe = dados["equipe"]
                nome = dados["nome"]
                lista_partes_nome = nome.split(" ")

                padrao_nome = re.compile(r"[A-Z][a-z]+")  # padrão (nome começa com letra maiúscula)
                lista_excecoes = (
                    "de", "da", "do", "dos", "das")  # partes de um nome que podem não começar com letra maiúscula

                index_for = 0
                for parte_nome in lista_partes_nome:
                    if not re.fullmatch(padrao_nome, parte_nome):  # se a parte do nome não atende o padrão
                        if parte_nome not in lista_excecoes:
                            return jsonify({"login": 40030})  # ela não pode não estar na lista de exceções
                        elif index_for == 0:
                            return jsonify({"login": 40030})  # nenhum nome começa com preposição
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
                    return jsonify({"login": 40010})

                user = User({
                    "nome": nome,
                    "senha": senha,
                    "id": usuario,
                    "equipe": equipe
                }, True)
                login_user(user)  # loga usuario
                return jsonify({"login": 20000})
            else:
                return jsonify({"login": 40001})
        else:
            dados = bd.child(f"usuarios/{usuario}").get().val()

            if not dados:
                return jsonify({"login": 40002})
            elif dados["senha"] != senha:
                return jsonify({"login": 40020})
            else:
                user = User(dados, False)
                login_user(user)
                return jsonify({"login": 20000})

    return render_template("login.html")


@app.route("/configurações", methods=["GET", "POST"])
@login_required
def configuracoes():
    nao_cadastrou_esportes = True if current_user.esportes_cadastrados == "" else False  # boolean se o usuario já cadastrou algum esporte
    if request.method == "POST":
        if request.form["tem_imagem"] == "true":
            imagem_bytes = request.files["imagem"].read()
            buffer = io.BytesIO(imagem_bytes)
            imagem = Image.open(buffer)
            # com a imagem iniciada na biblioteca pillow vou recorta-la para formar um quadrado perfeito, caso não seja
            largura, altura = imagem.size
            if altura != largura:
                if largura > altura:
                    quantidade_cortar_cada = int((largura - altura) / 2)
                    recorte_coordenadas = (quantidade_cortar_cada, 0, int(largura - quantidade_cortar_cada), altura)
                else:
                    quantidade_cortar_cada = int((altura - largura) / 2)
                    recorte_coordenadas = (0, quantidade_cortar_cada, largura, int(altura - quantidade_cortar_cada))

                imagem_formatada = imagem.crop(recorte_coordenadas)
            else:
                imagem_formatada = imagem

            buffer_png = io.BytesIO()
            imagem_formatada.save(buffer_png, format="PNG")
            # bytes_png = buffer_png.getvalue()
            # imagem_b64_png = base64.b64encode(bytes_png).decode("utf-8")
            buffer_png.seek(0)

            url_imagem = upload_image(buffer_png.getvalue(), f"fotos_de_perfil/{current_user.id}.png")

            bd.child(f"usuarios/{current_user.id}").update({"foto_de_perfil": url_imagem})
            current_user.foto_de_perfil = url_imagem
            if not nao_cadastrou_esportes:
                esportes = current_user.esportes_cadastrados
                index_for = 0
                for esporte in esportes:
                    pos = current_user.posicao[index_for]
                    bd.child(f"jogadores/{esporte}/{pos}/{current_user.id}").update({"foto_de_perfil": url_imagem})
                    index_for += 1

            if current_user.tem_foto_de_perfil_default:
                bd.child(f"usuarios/{current_user.id}").update({"tem_foto_de_perfil_default": False})
                current_user.tem_foto_de_perfil_default = False

        if nao_cadastrou_esportes:  # se o usuario não cadastrou roda o código
            inscrever_como_jogador = False if request.form["modalidade"] == "E" else True

            if inscrever_como_jogador:
                esportes = request.form["esportes_selecionados"]
                esportes = esportes.split(",")
                esportes_dict = {}
                index_for = 0
                for esporte in esportes:
                    posicao = "gol" if f"gol_{esporte}" in request.form else "ataque"

                    esportes_dict[str(index_for)] = esporte

                    bd.child(f"jogadores/{esporte}/{posicao}").update({
                        current_user.id: {
                            "foto_de_perfil": current_user.foto_de_perfil,
                            "nome": current_user.nome,
                            "equipe": current_user.equipe,
                            "pontos_ultima_partida": "",
                            "pontos_historico": ""
                        }
                    })
                    if current_user.posicao:
                        lista = current_user.posicao
                        lista[index_for] = posicao
                    else:
                        current_user.posicao = {0: posicao}

                    index_for += 1

                current_user.esportes_cadastrados = esportes_dict

                bd.child(f"usuarios/{current_user.id}").update({"esportes_cadastrados": esportes_dict})
                bd.child(f"usuarios/{current_user.id}").update({"posicao": current_user.posicao})

        return "sucesso"

    foto_de_perfil = current_user.foto_de_perfil
    id = current_user.id
    nome = current_user.nome

    return render_template("configuracoes.html", nome=nome, matricula=id, foto_de_perfil=foto_de_perfil,
                           nao_cadastrou_esportes=nao_cadastrou_esportes,
                           tem_foto_de_perfil_default=current_user.tem_foto_de_perfil_default)


def upload_image(imagem, path):
    # Faz o upload da imagem para o Firebase Storage diretamente do buffer
    storage.child(path).put(imagem)

    # Obtém a URL da imagem
    url = storage.child(path).get_url(None)
    return url


@app.route('/dados-do-banco/<info>', methods=['POST', 'GET'])
def dados_do_banco(info):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if info == "jogadores":
            dados = request.get_json()
            esporte = dados["esporte"]

            resposta = bd.child(f"jogadores/{esporte}").get().val()

            for posicao in resposta:
                jogadores_posicao = resposta[posicao]
                for jogador in jogadores_posicao:
                    historico_pontos = resposta[posicao][jogador].pop("pontos_historico")

                    if historico_pontos:
                        total_de_pontos = 0

                        index_for = 0
                        for pontos in historico_pontos:
                            total_de_pontos += pontos
                            index_for += 1
                        media_pontos = round((total_de_pontos / index_for), 1)
                    else:
                        media_pontos = ""

                    resposta[posicao][jogador]["media_pontos"] = media_pontos

            return jsonify(resposta)

        elif info == "escalacao":
            jogadores_cadastrados = bd.child(f"jogadores").get().val()
            dados_escalacao = bd.child(f"usuarios/{current_user.id}/escalacao").get().val()
            jogadores_escalados = []
            for esporte in dados_escalacao:
                escalacao_do_esporte = dados_escalacao[esporte]
                for posicao in escalacao_do_esporte:
                    if escalacao_do_esporte[posicao]:
                        jogadores_escalados.append(escalacao_do_esporte[posicao])

            jogadores_escalados = set(jogadores_escalados)

            fotos_jogadores_escalados = {}

            while len(fotos_jogadores_escalados) < len(jogadores_escalados):
                for esporte in jogadores_cadastrados:
                    dados_esporte = jogadores_cadastrados[esporte]
                    for posicao in dados_esporte:
                        jogadores = dados_esporte[posicao]
                        for jogador in jogadores:
                            if jogador in jogadores_escalados:
                                dados_jogador = jogadores[jogador]
                                fotos_jogadores_escalados[jogador] = dados_jogador["foto_de_perfil"]

            dados_return = {}
            for esporte in dados_escalacao:
                escalacao_do_esporte = dados_escalacao[esporte]
                dados_return[esporte] = {}
                for posicao in escalacao_do_esporte:
                    if escalacao_do_esporte[posicao]:
                        id_jogador = escalacao_do_esporte[posicao]
                        foto_jogador = fotos_jogadores_escalados[id_jogador]

                        dados_return[esporte][posicao] = [id_jogador, foto_jogador]

            pontuacao_atual_cada_esporte = bd.child(f"usuarios/{current_user.id}/pontos").get().val()

            for esporte in pontuacao_atual_cada_esporte:
                pontos = pontuacao_atual_cada_esporte[esporte]
                dados_return[esporte]["pontos"] = pontos

            return jsonify(dados_return)
    else:
        return "", 404


@app.route('/dados-do-banco/escalacao/<esporte>', methods=['POST', 'GET'])
def dados_do_banco_escalacao_especifica(esporte):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        dados_esporte = bd.child(f"jogadores/{esporte}").get().val()
        escalacao_do_esporte = bd.child(f"usuarios/{current_user.id}/escalacao/{esporte}").get().val()
        jogadores_escalados = []

        for posicao in escalacao_do_esporte:
            if escalacao_do_esporte[posicao]:
                jogadores_escalados.append(escalacao_do_esporte[posicao])

        fotos_jogadores_escalados = {}

        while len(fotos_jogadores_escalados) < len(jogadores_escalados):
            for posicao in dados_esporte:
                jogadores = dados_esporte[posicao]
                for jogador in jogadores:
                    if jogador in jogadores_escalados:
                        dados_jogador = jogadores[jogador]
                        fotos_jogadores_escalados[jogador] = dados_jogador["foto_de_perfil"]

        dados_return = {}
        for posicao in escalacao_do_esporte:
            if escalacao_do_esporte[posicao]:
                id_jogador = escalacao_do_esporte[posicao]
                foto_jogador = fotos_jogadores_escalados[id_jogador]

                dados_return[posicao] = [id_jogador, foto_jogador]

        pontuacao_atual_esporte = bd.child(f"usuarios/{current_user.id}/pontos/{esporte}").get().val()
        dados_return["pontos"] = pontuacao_atual_esporte

        return jsonify(dados_return)


@app.route("/ADM", methods=["GET", "POST"])
@login_required
def inserir_pontuao_redirect():
    administradores = bd.child("administracao/usuarios").get().val()

    if current_user.id in administradores:
        return redirect(url_for('ADM_autorizar'))
    else:
        return "", 404


@app.route("/ADM/<chave_secreta_fornecida>", methods=["GET", "POST"])
@login_required
def ADM(chave_secreta_fornecida=None):
    administradores = bd.child("administracao/usuarios").get().val()

    if current_user.id in administradores:
        form = ADMForm()
        mercado_atual = bd.child("mercado_aberto").get().val()

        for esporte in mercado_atual:
            if mercado_atual[esporte]:
                mercado_atual[esporte] = "Aberto"
            else:
                mercado_atual[esporte] = "Fechado"

        if request.method == "GET":
            if valida_chave_secreta_administracao(chave_secreta_fornecida):
                return render_template("ADM.html", form=form, chave_secreta=chave_secreta_fornecida, mercado_atual=mercado_atual)
            else:
                return "", 404
        elif form.validate_on_submit():
            if form.futsalM.data:
                return redirect(url_for('inserir_pontuacao_esporte', esporte="futsalM", chave_secreta_fornecida=chave_secreta_fornecida))
            elif form.futsalF.data:
                return redirect(url_for('inserir_pontuacao_esporte', esporte="futsalF", chave_secreta_fornecida=chave_secreta_fornecida))
            elif form.basquete.data:
                return redirect(url_for('inserir_pontuacao_esporte', esporte="basquete", chave_secreta_fornecida=chave_secreta_fornecida))
            elif form.handebol.data:
                return redirect(url_for('inserir_pontuacao_esporte', esporte="handebol", chave_secreta_fornecida=chave_secreta_fornecida))
            else:
                if valida_chave_secreta_administracao(chave_secreta_fornecida):
                    if form.alterar_mercado_futsalM.data:
                        booleano = bd.child("mercado_aberto/futsal_masculino").get().val()
                        bd.child("mercado_aberto/futsal_masculino").set(not booleano)

                        if not booleano:
                            mercado_atual["futsal_masculino"] = "Aberto"
                        else:
                            mercado_atual["futsal_masculino"] = "Fechado"

                        chave_secreta = troca_chave_secreta_administracao()

                        return render_template("ADM.html", form=form, chave_secreta=chave_secreta, mercado_atual=mercado_atual)
                    elif form.alterar_mercado_futsalF.data:
                        booleano = bd.child("mercado_aberto/futsal_feminino").get().val()
                        bd.child("mercado_aberto/futsal_feminino").set(not booleano)

                        if not booleano:
                            mercado_atual["futsal_feminino"] = "Aberto"
                        else:
                            mercado_atual["futsal_feminino"] = "Fechado"

                        chave_secreta = troca_chave_secreta_administracao()

                        return render_template("ADM.html", form=form, chave_secreta=chave_secreta, mercado_atual=mercado_atual)
                    elif form.alterar_mercado_basquete.data:
                        booleano = bd.child("mercado_aberto/basquete").get().val()
                        bd.child("mercado_aberto/basquete").set(not booleano)

                        if not booleano:
                            mercado_atual["basquete"] = "Aberto"
                        else:
                            mercado_atual["basquete"] = "Fechado"

                        chave_secreta = troca_chave_secreta_administracao()

                        return render_template("ADM.html", form=form, chave_secreta=chave_secreta, mercado_atual=mercado_atual)
                    elif form.alterar_mercado_handebol.data:
                        booleano = bd.child("mercado_aberto/handebol").get().val()
                        bd.child("mercado_aberto/handebol").set(not booleano)

                        if not booleano:
                            mercado_atual["hendebol"] = "Aberto"
                        else:
                            mercado_atual["hendebol"] = "Fechado"

                        chave_secreta = troca_chave_secreta_administracao()

                        return render_template("ADM.html", form=form, chave_secreta=chave_secreta, mercado_atual=mercado_atual)
                    else:
                        return "", 404
                else:
                    return "", 404

    else:
        return "", 404


@app.route("/ADM/autorizar", methods=["GET", "POST"])
@login_required
def ADM_autorizar():
    administradores = bd.child("administracao/usuarios").get().val()
    if current_user.id in administradores:
        form = ADMAutorizarForm()
        if request.method == "GET":
            setup_ADM_autorizar(administradores[current_user.id])

            return render_template("ADM-autorizar.html", erro="", form=form)

        elif form.validate_on_submit():
            codigo_fornecido = form.code.data
            form.code.data = ""

            codigo_desejado = session["code"]

            if codigo_fornecido == codigo_desejado:
                chave_secreta = bd.child("administracao/chave_de_acesso").get().val()
                return redirect(url_for("ADM", chave_secreta_fornecida=chave_secreta))
            else:
                setup_ADM_autorizar(administradores[current_user.id])

                return render_template("ADM-autorizar.html", erro=f"Código inválido, novo código enviado", form=form)
    else:
        return "", 404


def pontuar_esporte(form, esporte_a_pontuar):
    dados = {
        "jogador1": form.jogador1.data,
        "jogador2": form.jogador2.data,
        "jogador3": form.jogador3.data,
        "jogador4": form.jogador4.data,
        "jogador5": form.jogador5.data,
        "jogador6": form.jogador6.data,
        "jogador7": form.jogador7.data,
        "jogador8": form.jogador8.data
    }

    if esporte_a_pontuar != "basquete":
        modificador_de_pontos = 2

        if esporte_a_pontuar == "handebol":
            dados["jogador9"] = form.jogador9.data
            dados["jogador10"] = form.jogador10.data
            dados["jogador11"] = form.jogador11.data
            dados["jogador12"] = form.jogador12.data

        dados["goleiro1"] = form.goleiro1.data
        dados["goleiro2"] = form.goleiro2.data
    else:
        modificador_de_pontos = 1

        dados["jogador9"] = form.jogador9.data
        dados["jogador10"] = form.jogador10.data

    jogadores_com_mudancas = {}
    dados_atualizar = {}

    for jogador in dados:
        if dados[jogador]:
            pontos = 0
            id_jogador = dados[jogador]

            if "goleiro" in jogador:
                pontos_historico = bd.child(f"jogadores/{esporte_a_pontuar}/gol/{id_jogador}/pontos_historico").get().val()

                if jogador == "goleiro1":
                    gols = form.gols_goleiro1.data * 2
                    defesas = form.defesas_goleiro1.data * 2
                    amarelos = form.amarelos_goleiro1.data * -0.2
                    vermelho = form.vermelho_goleiro1.data * -3
                    faltas = form.faltas_goleiro1.data * -1
                    assistencias = form.assistencias_goleiro1.data * 0.5
                else:
                    gols = form.gols_goleiro2.data * 2
                    defesas = form.defesas_goleiro2.data * 2
                    amarelos = form.amarelos_goleiro2.data * -0.2
                    vermelho = form.vermelho_goleiro2.data * -3
                    faltas = form.faltas_goleiro2.data * -1
                    assistencias = form.assistencias_goleiro2.data * 0.5

                pontos = round(gols + amarelos + vermelho + faltas + assistencias, 1)

                if pontos_historico:
                    pontos_historico.append(pontos)
                else:
                    pontos_historico = [pontos, ]

                dados_atualizar[f"gol/{id_jogador}/pontos_ultima_partida"] = pontos
                dados_atualizar[f"gol/{id_jogador}/pontos_historico"] = pontos_historico

                jogadores_com_mudancas[id_jogador] = pontos
            else:
                pontos_historico = bd.child(f"jogadores/{esporte_a_pontuar}/ataque/{id_jogador}/pontos_historico").get().val()

                if "12" in jogador:
                    gols = form.pontos_jogador12.data * modificador_de_pontos
                    amarelos = form.amarelos_jogador12.data * -0.2
                    vermelho = form.vermelho_jogador12.data * -3
                    faltas = form.faltas_jogador12.data * -1
                    assistencias = form.assistencias_jogador12.data * 0.5

                elif "11" in jogador:
                    gols = form.pontos_jogador11.data * modificador_de_pontos
                    amarelos = form.amarelos_jogador11.data * -0.2
                    vermelho = form.vermelho_jogador11.data * -3
                    faltas = form.faltas_jogador11.data * -1
                    assistencias = form.assistencias_jogador11.data * 0.5
                elif "10" in jogador:
                    gols = form.pontos_jogador10.data * modificador_de_pontos
                    amarelos = form.amarelos_jogador10.data * -0.2
                    vermelho = form.vermelho_jogador10.data * -3
                    faltas = form.faltas_jogador10.data * -1
                    assistencias = form.assistencias_jogador10.data * 0.5
                elif "9" in jogador:
                    gols = form.pontos_jogador9.data * modificador_de_pontos
                    amarelos = form.amarelos_jogador9.data * -0.2
                    vermelho = form.vermelho_jogador9.data * -3
                    faltas = form.faltas_jogador9.data * -1
                    assistencias = form.assistencias_jogador9.data * 0.5
                elif "8" in jogador:
                    gols = form.pontos_jogador8.data * modificador_de_pontos
                    amarelos = form.amarelos_jogador8.data * -0.2
                    vermelho = form.vermelho_jogador8.data * -3
                    faltas = form.faltas_jogador8.data * -1
                    assistencias = form.assistencias_jogador8.data * 0.5
                elif "7" in jogador:
                    gols = form.pontos_jogador7.data * modificador_de_pontos
                    amarelos = form.amarelos_jogador7.data * -0.2
                    vermelho = form.vermelho_jogador7.data * -3
                    faltas = form.faltas_jogador7.data * -1
                    assistencias = form.assistencias_jogador7.data * 0.5
                elif "6" in jogador:
                    gols = form.pontos_jogador6.data * modificador_de_pontos
                    amarelos = form.amarelos_jogador6.data * -0.2
                    vermelho = form.vermelho_jogador6.data * -3
                    faltas = form.faltas_jogador6.data * -1
                    assistencias = form.assistencias_jogador6.data * 0.5
                elif "5" in jogador:
                    gols = form.pontos_jogador5.data * modificador_de_pontos
                    amarelos = form.amarelos_jogador5.data * -0.2
                    vermelho = form.vermelho_jogador5.data * -3
                    faltas = form.faltas_jogador5.data * -1
                    assistencias = form.assistencias_jogador5.data * 0.5
                elif "4" in jogador:
                    gols = form.pontos_jogador4.data * modificador_de_pontos
                    amarelos = form.amarelos_jogador4.data * -0.2
                    vermelho = form.vermelho_jogador4.data * -3
                    faltas = form.faltas_jogador4.data * -1
                    assistencias = form.assistencias_jogador4.data * 0.5
                elif "3" in jogador:
                    gols = form.pontos_jogador3.data * modificador_de_pontos
                    amarelos = form.amarelos_jogador3.data * -0.2
                    vermelho = form.vermelho_jogador3.data * -3
                    faltas = form.faltas_jogador3.data * -1
                    assistencias = form.assistencias_jogador3.data * 0.5
                elif "2" in jogador:
                    gols = form.pontos_jogador2.data * modificador_de_pontos
                    amarelos = form.amarelos_jogador2.data * -0.2
                    vermelho = form.vermelho_jogador2.data * -3
                    faltas = form.faltas_jogador2.data * -1
                    assistencias = form.assistencias_jogador2.data * 0.5
                else:
                    gols = form.pontos_jogador1.data * modificador_de_pontos
                    amarelos = form.amarelos_jogador1.data * -0.2
                    vermelho = form.vermelho_jogador1.data * -3
                    faltas = form.faltas_jogador1.data * -1
                    assistencias = form.assistencias_jogador1.data * 0.5

                pontos = round(gols + amarelos + vermelho + faltas + assistencias, 1)

                if pontos_historico:
                    pontos_historico.append(pontos)
                else:
                    pontos_historico = [pontos,]
                dados_atualizar[f"ataque/{id_jogador}/pontos_ultima_partida"] = pontos
                dados_atualizar[f"ataque/{id_jogador}/pontos_historico"] = pontos_historico

                jogadores_com_mudancas[id_jogador] = pontos

    bd.child(f"jogadores/{esporte_a_pontuar}").update(dados_atualizar)

    usuarios = bd.child("usuarios").get().val()
    dados_atualizar_usuarios = {}
    for usuario in usuarios:
        pontuacao_a_adicionar = 0

        escalacao_do_esporte = usuarios[usuario]["escalacao"][esporte_a_pontuar]
        for posicao in escalacao_do_esporte:
            jogador = escalacao_do_esporte[posicao]

            for jogador_com_mudanca in jogadores_com_mudancas:
                if jogador_com_mudanca == jogador:
                    pontuacao_a_adicionar += jogadores_com_mudancas[jogador_com_mudanca]

        if pontuacao_a_adicionar != 0:
            pontuacao_atual = usuarios[usuario]["pontos"][esporte_a_pontuar]
            pontuacao_final = pontuacao_atual + pontuacao_a_adicionar
            dados_atualizar_usuarios[f"{usuario}/pontos/{esporte_a_pontuar}"] = pontuacao_final

    bd.child("usuarios").update(dados_atualizar_usuarios)

    return troca_chave_secreta_administracao()


@app.route("/inserir-pontuacao/<esporte>/<chave_secreta_fornecida>", methods=["GET", "POST"])
@login_required
def inserir_pontuacao_esporte(esporte, chave_secreta_fornecida=None):
    chave_bd = bd.child("administracao/chave_de_acesso").get().val()

    if esporte == "futsalM":
        form = InserirPontuacaoFormFutsalM()
    elif esporte == "futsalF":
        form = InserirPontuacaoFormFutsalF()
    elif esporte == "basquete":
        form = InserirPontuacaoFormBasquete()
    elif esporte == "handebol":
        form = InserirPontuacaoFormHandebol()
    else:
        return "", 404

    if request.method == "GET":
        if chave_bd == chave_secreta_fornecida:
            return render_template("inserir-pontuacao-esporte.html",
                                   form=form,
                                   esporte=esporte,
                                   chave_secreta_fornecida=chave_secreta_fornecida)
        else:
            return "", 404
    elif form.validate_on_submit():
        esporte_a_pontuar = form.nome_esporte.data

        nova_chave_secreta = pontuar_esporte(form, esporte_a_pontuar)

        return redirect(url_for("ADM", chave_secreta_fornecida=nova_chave_secreta))


@app.route("/leaderboards", methods=["GET"])
def leaderboards():
    usuarios = bd.child("usuarios").get().val()
    dados_por_pontos = {}
    pontos_equipes = {
        "asia": 0,
        "africa": 0,
        "america": 0
    }
    for usuario in usuarios:
        qtd_pontos = 0
        dados_pontos = usuarios[usuario]["pontos"]

        for esporte in dados_pontos:
            qtd_pontos += float(dados_pontos[esporte])

        nome = usuarios[usuario]["nome"]
        equipe = usuarios[usuario]["equipe"]
        foto_de_perfil = usuarios[usuario]["foto_de_perfil"]

        pontos_equipes[equipe] += qtd_pontos

        dados_por_pontos[qtd_pontos] = [nome, equipe, foto_de_perfil]

    dados_envio = {}
    index_for = 1
    for pontuacao in sorted(dados_por_pontos, reverse=True):
        dados_usuario = dados_por_pontos[pontuacao]
        dados_usuario.append(pontuacao)

        dados_envio[index_for] = dados_usuario

        if index_for == 50:
            break

        index_for += 1

    pontos_equipes_str = {}
    for equipe in pontos_equipes:
        pontos_equipes_str[equipe] = str(int(pontos_equipes[equipe]))

    return render_template("leaderboards.html", dados=dados_envio, pontos_equipes=pontos_equipes, pontos_equipes_str=pontos_equipes_str)


def valida_chave_secreta_administracao(chave_fornecida):
    chave_secreta_bd = bd.child("administracao/chave_de_acesso").get().val()
    if chave_fornecida == chave_secreta_bd:
        return True
    else:
        return False


def troca_chave_secreta_administracao():
    caracteres = string.ascii_letters + string.digits
    nova_chave = "".join([secrets.choice(caracteres) for _ in range(32)])
    bd.child("administracao/chave_de_acesso").set(nova_chave)

    return nova_chave


def setup_ADM_autorizar(email_adm):
    numeros = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0")

    numeros_escolhidos = [secrets.choice(numeros) for _ in range(6)]
    codigo = "".join(numeros_escolhidos)

    session["code"] = codigo

    corpo_email = f"<p>Seu código de verificação é: {codigo}</p>"

    msg = email.message.Message()

    msg['Subject'] = "Código de verificação"
    msg['From'] = os.getenv("EMAIL_VERIFICACAO")
    msg['To'] = email_adm
    password = os.getenv("GMAIL_SENHA_APP")
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email)

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))


if __name__ == '__main__':
    app.run(debug=True)


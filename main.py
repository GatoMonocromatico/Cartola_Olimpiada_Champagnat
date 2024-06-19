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
            self.foto_de_perfil = "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"
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


from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/configurações", methods=["GET", "POST"])
def configuracoes():
    return render_template("configuracoes.html")


if __name__ == '__main__':
    app.run(debug=True)


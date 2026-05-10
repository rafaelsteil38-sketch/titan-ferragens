from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# =========================
# CONFIGURAÇÃO DO APP
# =========================

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# =========================
# MODELO DO BANCO
# =========================

class Produto(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(
        db.String(100),
        nullable=False
    )

    preco = db.Column(
        db.String(50),
        nullable=False
    )

    descricao = db.Column(
        db.Text,
        nullable=False
    )

    imagem = db.Column(
        db.String(500),
        nullable=False
    )

# =========================
# PÁGINA INICIAL
# =========================

@app.route("/")
def index():

    produtos = Produto.query.all()

    return render_template(
        "index.html",
        produtos=produtos
    )

# =========================
# PRODUTOS
# =========================

@app.route("/produtos")
def produtos():

    produtos = Produto.query.all()

    return render_template(
        "produtos.html",
        produtos=produtos
    )

# =========================
# SOBRE
# =========================

@app.route("/sobre")
def sobre():

    return render_template("sobre.html")

# =========================
# CONTATO
# =========================

@app.route("/contato")
def contato():

    return render_template("contato.html")

# =========================
# ADMIN
# =========================

@app.route("/admin", methods=["GET", "POST"])
def admin():

    if request.method == "POST":

        nome = request.form.get("nome")

        preco = request.form.get("preco")

        descricao = request.form.get("descricao")

        imagem = request.form.get("imagem")

        novo_produto = Produto(
            nome=nome,
            preco=preco,
            descricao=descricao,
            imagem=imagem
        )

        db.session.add(novo_produto)

        db.session.commit()

        return redirect(url_for("admin"))

    produtos = Produto.query.all()

    return render_template(
        "admin.html",
        produtos=produtos
    )

# =========================
# DELETAR PRODUTO
# =========================

@app.route("/deletar/<int:id>")
def deletar(id):

    produto = Produto.query.get_or_404(id)

    db.session.delete(produto)

    db.session.commit()

    return redirect(url_for("admin"))

# =========================
# INICIAR SERVIDOR
# =========================

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
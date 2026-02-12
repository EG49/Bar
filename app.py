from flask import Flask, render_template

app = Flask(__name__)
@app.context_processor
def inject_user():
    user = {"nombre": "Evans"}  # solo para prueba
    return dict(user=user)
@app.route("/inicio")
def inicio():
    return render_template("inicio.html")

@app.route("/vender")
def vender():
    return render_template("vender.html")

@app.route("/nuevosClientes")
def nuevosClientes():
    return render_template("nuevosClientes.html")

@app.route("/facturas")
def facturas():
    return render_template("facturas.html")

@app.route("/productos")
def productos():
    return render_template("productos.html")

@app.route("/cuentas")
def cuentas():
    return render_template("cuentas.html")

@app.route("/cobrar")
def cobrar():
    return render_template("cobrar.html")

@app.route("/pedidos")
def pedidos():
    return render_template("pedidos.html")

@app.route("/")
def login():
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)

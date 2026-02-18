from flask import Flask, render_template, request, jsonify, session, redirect, url_for, session 
from  config import get_connection
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("show_login"))
        return f(*args, **kwargs)
    return decorated_function


app = Flask(__name__)
print(app.url_map)
app.secret_key = "super_secret_key"

@app.context_processor
def inject_user():
    user = {"nombre": "Evans"}  # solo para prueba
    return dict(user=user)
@app.route("/inicio")
@login_required
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

@app.route("/", methods=["GET"])
def show_login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def process_login():
    username = request.form.get("username")
    password = request.form.get("password")

    try:
        conn = get_connection()
        cur = conn.cursor()

        query = """
            SELECT id, username, rol, debe_cambiar_password, otp_activo
            FROM usuarios
            WHERE username = %s
              AND estado = TRUE
              AND password_hash = crypt(%s, password_hash);
        """

        cur.execute(query, (username, password))
        user = cur.fetchone()

        if user:
            session["user_id"] = user[0]
            session["username"] = user[1]
            session["rol"] = user[2]

            cur.execute(
                "UPDATE usuarios SET ultimo_login = NOW() WHERE id = %s;",
                (user[0],)
            )
            conn.commit()

            cur.close()
            conn.close()

            return redirect("/inicio")



        cur.close()
        conn.close()

        return "Credenciales inválidas", 401

    except Exception as e:
        return str(e), 500

#a
# -----------------------
# 3️⃣ Dashboard
# -----------------------

 

if __name__ == "__main__":
    app.run(debug=True)

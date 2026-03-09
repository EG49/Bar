from flask import Flask, render_template, request, jsonify, session, redirect, url_for, session 
from  config import get_connection
from functools import wraps
from email_service import enviar_correo
from datetime import datetime

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
            SELECT id, username, email, rol, debe_cambiar_password, otp_activo, nombre
            FROM usuarios
            WHERE username = %s
              AND estado = TRUE
              AND password_hash = crypt(%s, password_hash);
        """

        cur.execute(query, (username, password))
        user = cur.fetchone()

        if user:

            session["user"] = {
                                "id": user[0],
                                "username": user[1],
                                "nombre": user[6],
                                "rol": user[3]
                            }

            email = user[2]

            # actualizar último login
            cur.execute(
                "UPDATE usuarios SET ultimo_login = NOW() WHERE id = %s;",
                (user[0],)
            )

            conn.commit()

            # enviar correo de notificación
            ip = request.remote_addr
            user_agent = request.headers.get('User-Agent')
            sistema, navegador = detectar_dispositivo(user_agent)
            mensaje = f"""
            <h2>🚨 Alerta de seguridad 🚨</h2>

            <p>Hola {user[1]},</p>

            <p>Detectamos un <b>nuevo inicio de sesión</b> en tu cuenta.</p>

            <hr>

            <p><b>👤 Usuario:</b> {user[1]}</p>
            <p><b>📅 Fecha:</b> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            <p><b>🌐 IP:</b> {ip}</p>
            <p><b>{sistema}</b></p>
            <p><b>{navegador}</b></p>

            <hr>

            <p>✅ Si fuiste tú, puedes ignorar este mensaje.</p>

            <p style="color:red;">
            ⚠️ Si no reconoces esta actividad, cambia tu contraseña inmediatamente.
            </p>

            <p>— Sistema de prueba Evans</p>
            """

            enviar_correo(
                email,
                "Inicio de sesión detectado",
                mensaje
            )

            cur.close()
            conn.close()

            return redirect("/inicio")

        cur.close()
        conn.close()

        return "Credenciales inválidas", 401

    except Exception as e:
        return str(e), 500

@app.context_processor
def inject_user():
    print(session.get("user"))
    return dict(user=session.get("user"))

def detectar_dispositivo(user_agent):

    ua = user_agent.lower()

    # Sistema / dispositivo
    if "windows" in ua:
        sistema = "💻 Windows"
    elif "mac os" in ua or "macintosh" in ua:
        sistema = "💻 Mac"
    elif "linux" in ua:
        sistema = "💻 Linux"
    elif "android" in ua:
        sistema = "📱 Android"
    elif "iphone" in ua or "ipad" in ua:
        sistema = "📱 iPhone / iPad"
    else:
        sistema = "💻 Dispositivo desconocido"

    # Navegador
    if "chrome" in ua and "edg" not in ua:
        navegador = "🌐 Chrome"
    elif "firefox" in ua:
        navegador = "🌐 Firefox"
    elif "safari" in ua and "chrome" not in ua:
        navegador = "🌐 Safari"
    elif "edg" in ua:
        navegador = "🌐 Edge"
    else:
        navegador = "🌐 Navegador desconocido"

    return sistema, navegador


#a
# -----------------------
# 3️⃣ Dashboard
# -----------------------

 

if __name__ == "__main__":
    app.run(debug=True)

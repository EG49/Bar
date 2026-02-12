from flask import Flask, render_template

app = Flask(__name__)
@app.route("/login")
def login():
    return render_template("login.html")
@app.route("/inicio")
def inicio():
    user = {"nombre": "Evans"}  # ejemplo
    return render_template("inicio.html", user=user)

if __name__ == "__main__":
    app.run(debug=True)

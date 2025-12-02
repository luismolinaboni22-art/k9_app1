from flask import Flask, render_template, redirect, url_for, request, session
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "clave_super_secreta_para_sessions"

# Credenciales del admin
ADMIN_USER = "jorgemolinabonilla@gmail.com"
ADMIN_PASSWORD = "123"

# Lista temporal de visitantes en sitio (luego se pasa a BD)
visitantes_en_sitio = []


# ---------- LOGIN ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form.get("email")
        password = request.form.get("password")

        if user == ADMIN_USER and password == ADMIN_PASSWORD:
            session["user"] = user  # <--- CORREGIDO
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Usuario o contraseña incorrectos")

    return render_template("login.html")


# ---------- DASHBOARD ----------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    return render_template("dashboard.html")


# ---------- REGISTRAR VISITANTE ----------
@app.route("/registrar", methods=["GET", "POST"])
def registrar():
    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":
        visitante = {
            "id": len(visitantes_en_sitio) + 1,
            "nombre": request.form["nombre"],
            "cedula": request.form["cedula"],
            "empresa": request.form["empresa"],
            "persona_visita": request.form["persona_visita"],
            "proposito": request.form["proposito"],
            "placa": request.form["placa"],
            "induccion": request.form["induccion"],
            "hora_entrada": datetime.now().strftime("%H:%M"),
            "hora_salida": None
        }

        visitantes_en_sitio.append(visitante)

        return render_template("registrar.html", success=True)

    return render_template("registrar.html")


# ---------- LISTA DE VISITANTES EN SITIO ----------
@app.route("/en-sitio")
def en_sitio():
    if "user" not in session:
        return redirect("/login")

    return render_template("en_sitio.html", visitantes=visitantes_en_sitio)


# ---------- REGISTRAR SALIDA ----------
@app.route("/salida/<int:id>")
def salida(id):
    if "user" not in session:
        return redirect("/login")

    for v in visitantes_en_sitio:
        if v["id"] == id:
            v["hora_salida"] = datetime.now().strftime("%H:%M")
            visitantes_en_sitio.remove(v)
            break

    return redirect("/en-sitio")


# ---------- HOME ----------
@app.route("/")
def index():
    if "user" not in session:
        return redirect("/login")
    return redirect("/dashboard")


# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# ---------- CONFIG RENDER ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


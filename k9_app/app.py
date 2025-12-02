from flask import Flask, render_template, redirect, url_for, request, session, flash
from datetime import datetime
import os
from models import db, Visitante  # Importa el modelo

app = Flask(__name__)
app.secret_key = "clave_super_secreta_para_sessions"

# ---------- CONFIGURACIÓN DE BASE DE DATOS ----------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///visitantes.db'  # Cambiar a PostgreSQL si se desea
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Crear tablas al iniciar la app
with app.app_context():
    db.create_all()

# ---------- CREDENCIALES DEL ADMIN ----------
ADMIN_USER = "jorgemolinabonilla@gmail.com"
ADMIN_PASSWORD = "123"

# ---------- LOGIN ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form.get("email")
        password = request.form.get("password")

        if user == ADMIN_USER and password == ADMIN_PASSWORD:
            session["user"] = user
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

# ---------- REGISTRAR VISITANTES ----------
@app.route("/visitantes", methods=["GET", "POST"])
def visitantes():
    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":
        # Registro de ingreso
        nombre = request.form.get("nombre")
        cedula = request.form.get("cedula")
        empresa = request.form.get("empresa")
        persona_visita = request.form.get("persona_visita")
        motivo = request.form.get("motivo")
        placa = request.form.get("placa")

        if not nombre or not cedula or not persona_visita:
            flash("Nombre, cédula y persona a quien visita son obligatorios", "error")
        else:
            nuevo = Visitante(
                nombre=nombre,
                cedula=cedula,
                empresa=empresa,
                persona_visita=persona_visita,
                motivo=motivo,
                placa=placa
            )
            db.session.add(nuevo)
            db.session.commit()
            flash(f"Visitante {nombre} registrado correctamente", "success")
            return redirect(url_for("visitantes"))

    visitantes_lista = Visitante.query.order_by(Visitante.hora_ingreso.desc()).all()
    return render_template("visitantes.html", visitantes=visitantes_lista)

# ---------- REGISTRAR SALIDA ----------
@app.route("/salida/<int:id>")
def salida(id):
    if "user" not in session:
        return redirect("/login")

    visitante = Visitante.query.get(id)
    if visitante and not visitante.hora_salida:
        visitante.hora_salida = datetime.utcnow()
        db.session.commit()

    return redirect(url_for("visitantes"))

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

# ---------- RUN APP ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

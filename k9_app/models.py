from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Visitante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    cedula = db.Column(db.String(50), nullable=False)
    empresa = db.Column(db.String(100), nullable=True)
    persona_visita = db.Column(db.String(100), nullable=False)
    motivo = db.Column(db.String(200), nullable=True)
    placa = db.Column(db.String(20), nullable=True)
    hora_ingreso = db.Column(db.DateTime, default=datetime.utcnow)
    hora_salida = db.Column(db.DateTime, nullable=True)


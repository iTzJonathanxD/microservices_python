from app.database import db

class Cliente(db.Model):
    __tablename__ = "clientes"
    id_cliente = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    nombre_cliente = db.Column(db.String(100), nullable=False)
    telefono_cliente = db.Column(db.String(15), nullable=False)

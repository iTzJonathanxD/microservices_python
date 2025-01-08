from app.database import db

class Reserva(db.Model):
    __tablename__ = "reservas"
    id_reserva = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    fecha_reserva = db.Column(db.Date, nullable=False)
    id_cliente = db.Column(db.BigInteger, db.ForeignKey("clientes.id_cliente", ondelete="CASCADE"), nullable=False)

    cliente = db.relationship("Cliente", backref=db.backref("reservas", cascade="all, delete-orphan"))


class Cliente(db.Model):
    __tablename__ = "clientes"
    id_cliente = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    nombre_cliente = db.Column(db.String(100), nullable=False)
    telefono_cliente = db.Column(db.String(15), nullable=False)

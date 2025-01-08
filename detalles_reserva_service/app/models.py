from app.database import db


class Cliente(db.Model):
    __tablename__ = "clientes"
    id_cliente = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    nombre_cliente = db.Column(db.String(100), nullable=False)
    telefono_cliente = db.Column(db.String(15), nullable=False)


class Reserva(db.Model):
    __tablename__ = "reservas"
    id_reserva = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    fecha_reserva = db.Column(db.Date, nullable=False)
    id_cliente = db.Column(db.BigInteger, db.ForeignKey("clientes.id_cliente", ondelete="CASCADE"), nullable=False)

    cliente = db.relationship("Cliente", backref=db.backref("reservas", cascade="all, delete-orphan"))


class Menu(db.Model):
    __tablename__ = "menu"
    id_menu = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    nombre_menu = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=False)


class DetalleReserva(db.Model):
    __tablename__ = "detalles_reserva"
    id_detalle_reserva = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    id_reserva = db.Column(db.BigInteger, db.ForeignKey("reservas.id_reserva", ondelete="CASCADE"), nullable=False)
    id_menu = db.Column(db.BigInteger, db.ForeignKey("menu.id_menu", ondelete="CASCADE"), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False, default=1)

    reserva = db.relationship("Reserva", backref=db.backref("detalles", cascade="all, delete-orphan"))
    menu = db.relationship("Menu", backref=db.backref("detalles", cascade="all, delete-orphan"))

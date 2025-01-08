import strawberry
from sqlalchemy.orm import Session
from app.models import Cliente, Reserva
from app.database import db

@strawberry.type
class ClienteType:
    id: int
    nombre: str
    telefono: str


@strawberry.type
class ReservaType:
    id: int
    fecha: str
    cliente: ClienteType


@strawberry.type
class Query:
    @strawberry.field
    def get_clientes(self) -> list[ClienteType]:
        clientes = Cliente.query.all()
        return [ClienteType(id=c.id_cliente, nombre=c.nombre_cliente, telefono=c.telefono_cliente) for c in clientes]

    @strawberry.field
    def get_cliente(self, id_cliente: int) -> ClienteType:
        cliente = Cliente.query.get_or_404(id_cliente)
        return ClienteType(id=cliente.id_cliente, nombre=cliente.nombre_cliente, telefono=cliente.telefono_cliente)

    @strawberry.field
    def get_reservas(self) -> list[ReservaType]:
        reservas = Reserva.query.all()
        return [
            ReservaType(
                id=r.id_reserva,
                fecha=r.fecha_reserva.strftime("%Y-%m-%d"),
                cliente=ClienteType(
                    id=r.cliente.id_cliente,
                    nombre=r.cliente.nombre_cliente,
                    telefono=r.cliente.telefono_cliente
                )
            )
            for r in reservas
        ]

    @strawberry.field
    def get_reserva(self, id_reserva: int) -> ReservaType:
        reserva = Reserva.query.get_or_404(id_reserva)
        return ReservaType(
            id=reserva.id_reserva,
            fecha=reserva.fecha_reserva.strftime("%Y-%m-%d"),
            cliente=ClienteType(
                id=reserva.cliente.id_cliente,
                nombre=reserva.cliente.nombre_cliente,
                telefono=reserva.cliente.telefono_cliente
            )
        )


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_cliente(self, nombre: str, telefono: str) -> ClienteType:
        cliente = Cliente(nombre_cliente=nombre, telefono_cliente=telefono)
        db.session.add(cliente)
        db.session.commit()
        return ClienteType(id=cliente.id_cliente, nombre=cliente.nombre_cliente, telefono=cliente.telefono_cliente)

    @strawberry.mutation
    def update_cliente(self, id_cliente: int, nombre: str = None, telefono: str = None) -> ClienteType:
        cliente = Cliente.query.get_or_404(id_cliente)
        if nombre:
            cliente.nombre_cliente = nombre
        if telefono:
            cliente.telefono_cliente = telefono
        db.session.commit()
        return ClienteType(id=cliente.id_cliente, nombre=cliente.nombre_cliente, telefono=cliente.telefono_cliente)

    @strawberry.mutation
    def delete_cliente(self, id_cliente: int) -> str:
        cliente = Cliente.query.get_or_404(id_cliente)
        db.session.delete(cliente)
        db.session.commit()
        return f"Cliente con ID {id_cliente} eliminado exitosamente."

    @strawberry.mutation
    def create_reserva(self, fecha: str, id_cliente: int) -> ReservaType:
        cliente = Cliente.query.get_or_404(id_cliente)
        reserva = Reserva(fecha_reserva=fecha, id_cliente=id_cliente)
        db.session.add(reserva)
        db.session.commit()
        return ReservaType(
            id=reserva.id_reserva,
            fecha=reserva.fecha_reserva.strftime("%Y-%m-%d"),
            cliente=ClienteType(
                id=cliente.id_cliente,
                nombre=cliente.nombre_cliente,
                telefono=cliente.telefono_cliente
            )
        )

    @strawberry.mutation
    def update_reserva(self, id_reserva: int, fecha: str = None, id_cliente: int = None) -> ReservaType:
        reserva = Reserva.query.get_or_404(id_reserva)
        if fecha:
            reserva.fecha_reserva = fecha
        if id_cliente:
            cliente = Cliente.query.get_or_404(id_cliente)
            reserva.id_cliente = id_cliente
        db.session.commit()
        return ReservaType(
            id=reserva.id_reserva,
            fecha=reserva.fecha_reserva.strftime("%Y-%m-%d"),
            cliente=ClienteType(
                id=reserva.cliente.id_cliente,
                nombre=reserva.cliente.nombre_cliente,
                telefono=reserva.cliente.telefono_cliente
            )
        )

    @strawberry.mutation
    def delete_reserva(self, id_reserva: int) -> str:
        reserva = Reserva.query.get_or_404(id_reserva)
        db.session.delete(reserva)
        db.session.commit()
        return f"Reserva con ID {id_reserva} eliminada exitosamente."


schema = strawberry.Schema(query=Query, mutation=Mutation)

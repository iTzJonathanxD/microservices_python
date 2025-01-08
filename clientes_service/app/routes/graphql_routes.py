import strawberry
from sqlalchemy.orm import Session
from app.models import Cliente
from app.database import db

@strawberry.type
class ClienteType:
    id: int
    nombre: str
    telefono: str

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

schema = strawberry.Schema(query=Query, mutation=Mutation)

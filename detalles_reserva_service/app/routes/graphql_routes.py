import strawberry
from sqlalchemy.orm import Session
from app.models import DetalleReserva, Reserva, Menu
from app.database import db

@strawberry.type
class DetalleReservaType:
    id: int
    id_reserva: int
    id_menu: int
    cantidad: int
    menu_nombre: str
    reserva_fecha: str


@strawberry.type
class Query:
    @strawberry.field
    def get_detalles_reserva(self) -> list[DetalleReservaType]:
        detalles = DetalleReserva.query.all()
        return [
            DetalleReservaType(
                id=d.id_detalle_reserva,
                id_reserva=d.id_reserva,
                id_menu=d.id_menu,
                cantidad=d.cantidad,
                menu_nombre=d.menu.nombre_menu,
                reserva_fecha=d.reserva.fecha_reserva.strftime("%Y-%m-%d")
            )
            for d in detalles
        ]

    @strawberry.field
    def get_detalle_reserva(self, id_detalle_reserva: int) -> DetalleReservaType:
        detalle = DetalleReserva.query.get_or_404(id_detalle_reserva)
        return DetalleReservaType(
            id=detalle.id_detalle_reserva,
            id_reserva=detalle.id_reserva,
            id_menu=detalle.id_menu,
            cantidad=detalle.cantidad,
            menu_nombre=detalle.menu.nombre_menu,
            reserva_fecha=detalle.reserva.fecha_reserva.strftime("%Y-%m-%d")
        )


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_detalle_reserva(
        self, id_reserva: int, id_menu: int, cantidad: int
    ) -> DetalleReservaType:
        # Verificar existencia de la reserva
        reserva = Reserva.query.get_or_404(id_reserva)

        # Verificar existencia del menú
        menu = Menu.query.get_or_404(id_menu)

        detalle = DetalleReserva(
            id_reserva=id_reserva,
            id_menu=id_menu,
            cantidad=cantidad,
        )
        db.session.add(detalle)
        db.session.commit()
        return DetalleReservaType(
            id=detalle.id_detalle_reserva,
            id_reserva=detalle.id_reserva,
            id_menu=detalle.id_menu,
            cantidad=detalle.cantidad,
            menu_nombre=menu.nombre_menu,
            reserva_fecha=reserva.fecha_reserva.strftime("%Y-%m-%d"),
        )

    @strawberry.mutation
    def update_detalle_reserva(
        self,
        id_detalle_reserva: int,
        id_reserva: int = None,
        id_menu: int = None,
        cantidad: int = None,
    ) -> DetalleReservaType:
        detalle = DetalleReserva.query.get_or_404(id_detalle_reserva)

        if id_reserva:
            reserva = Reserva.query.get_or_404(id_reserva)
            detalle.id_reserva = id_reserva

        if id_menu:
            menu = Menu.query.get_or_404(id_menu)
            detalle.id_menu = id_menu

        if cantidad is not None:
            detalle.cantidad = cantidad

        db.session.commit()

        return DetalleReservaType(
            id=detalle.id_detalle_reserva,
            id_reserva=detalle.id_reserva,
            id_menu=detalle.id_menu,
            cantidad=detalle.cantidad,
            menu_nombre=detalle.menu.nombre_menu,
            reserva_fecha=detalle.reserva.fecha_reserva.strftime("%Y-%m-%d"),
        )

    @strawberry.mutation
    def delete_detalle_reserva(self, id_detalle_reserva: int) -> str:
        detalle = DetalleReserva.query.get_or_404(id_detalle_reserva)
        db.session.delete(detalle)
        db.session.commit()
        return f"Detalle de reserva con ID {id_detalle_reserva} eliminado exitosamente."


schema = strawberry.Schema(query=Query, mutation=Mutation)

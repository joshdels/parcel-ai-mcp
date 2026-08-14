from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.db.models import Parcel


def get_parcels(
    session: Session,
    min_acres: float | None = None,
    max_acres: float | None = None,
    min_value: float | None = None,
    max_value: float | None = None,
):
    """Retrieves parcels with calculated acreage or market_value."""

    area_acres = func.ST_Area(func.ST_Transform(Parcel.geom, 2277)) / 43560

    statement = select(
        Parcel,
        area_acres.label("area_acres"),
        func.ST_AsGeoJSON(Parcel.geom).label("geojson"),
    )

    if min_acres is not None:
        statement = statement.where(area_acres >= min_acres)

    if max_acres is not None:
        statement = statement.where(area_acres <= max_acres)

    if min_value is not None:
        statement = statement.where(Parcel.mkt_value >= min_value)

    if max_value is not None:
        statement = statement.where(Parcel.mkt_value <= max_value)

    statement = statement.limit(20)

    return session.execute(statement)


def get_parcel_by_prop_id(session: Session, prop_id: str):
    """Retrieves a parcel by property ID."""

    area_acres = func.ST_Area(func.ST_Transform(Parcel.geom, 2277)) / 43560

    geometry = func.ST_AsGeoJSON(func.ST_Transform(Parcel.geom, 4326))

    statement = select(
        Parcel.prop_id,
        area_acres.label("area_acres"),
        geometry.label("geometry"),
    ).where(Parcel.prop_id == prop_id)

    return session.execute(statement).first()


def count_all_parcels(session: Session):
    """Returns a total number of parcels."""

    statement = select(func.count()).select_from(Parcel)

    return session.scalar(statement)

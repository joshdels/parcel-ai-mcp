from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.db.models import Parcel


def get_all_parcels(session: Session):
    """Retrieves all parcels information."""

    statement = select(Parcel).limit(20)

    return session.scalars(statement).all()


def get_parcel_by_prop_id(session: Session, prop_id: str):
    """Retrieves a parcel by property ID."""

    statement = select(Parcel).where(Parcel.prop_id.ilike(prop_id))

    return session.scalars(statement).first()


def count_all_parcels(session: Session):
    """Returns a total number of parcels."""

    statement = select(func.count()).select_from(Parcel)

    return session.scalar(statement)

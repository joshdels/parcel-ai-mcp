from sqlalchemy import String, Integer, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from geoalchemy2 import Geometry


class Base(DeclarativeBase):
    pass


class Parcel(Base):
    __tablename__ = "williamson_parcels"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    prop_id: Mapped[str] = mapped_column(String)
    owner_name: Mapped[str] = mapped_column(String)
    mkt_value: Mapped[float] = mapped_column(Float)
    situs_addr: Mapped[str] = mapped_column(String)

    geom: Mapped[Geometry] = mapped_column(
        Geometry("MULTIPOLYGON", srid=4326),
        index=True,
    )

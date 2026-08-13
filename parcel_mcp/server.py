import sys

from pathlib import Path
from mcp.server import MCPServer
from sqlalchemy.orm import Session

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.db.database import engine
from app.service.queries import (
    get_all_parcels,
    get_parcel_by_prop_id,
    count_all_parcels,
)

mcp = MCPServer("WilliamsonParcelBot")


@mcp.tool()
def list_parcels():
    with Session(engine) as session:
        parcels = get_all_parcels(session)

        return [
            {
                "property_id": parcel.prop_id,
                "owner_name": parcel.owner_name,
                "market_value": parcel.mkt_value,
                "situs_address": parcel.situs_addr,
                "geom": parcel.geom,
            }
            for parcel in parcels
        ]


@mcp.tool()
def find_parcel_by_prop_id(prop_id: str):
    with Session(engine) as session:
        parcel = get_parcel_by_prop_id(session, prop_id)

        if parcel is None:

            return {
                "found": False,
                "message": f"No parcel found with property ID '{prop_id}'.",
            }

        return [
            {
                "property_id": parcel.prop_id,
                "owner_name": parcel.owner_name,
                "market_value": parcel.mkt_value,
                "situs_address": parcel.situs_addr,
                "geom": parcel.geom,
            }
        ]


@mcp.tool()
def get_count_parcels():
    with Session(engine) as session:
        count = count_all_parcels(session)

        return [{"parcel_count": count}]

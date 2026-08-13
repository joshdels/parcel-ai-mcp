import json
import sys

from pathlib import Path
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.db.database import get_session
from app.service.queries import get_all_parcels

app = FastAPI()


@app.get("/parcels")
def parcels(
    min_acres: float | None = None,
    max_acres: float | None = None,
    session: Session = Depends(get_session),
):
    parcels = get_all_parcels(session, min_acres, max_acres)

    return [
        {
            "property_id": parcel.prop_id,
            "owner_name": parcel.owner_name,
            "market_value": parcel.mkt_value,
            "situs_address": parcel.situs_addr,
            "geom": json.loads(geojson) if geojson else None,
        }
        for parcel, geojson in parcels
    ]

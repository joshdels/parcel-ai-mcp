import json

from pydantic import BaseModel
from fastapi import Depends, FastAPI, WebSocket, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.db.database import get_session
from app.service.queries import get_parcel_by_prop_id


class MapCommand(BaseModel):
    action: str
    parcel_id: str


browser_socket = None

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TILE_SQL = text("""
    SELECT ST_AsMVT(tile, 'williamson_parcels')
    FROM (
        SELECT
            prop_id,
            mkt_value,
            owner_name,
            situs_addr,

            ST_AsMVTGeom(
                geom_3857,
                ST_TileEnvelope(:z, :x, :y),
                4096,
                64,
                true
            ) AS geom
        FROM williamson_parcels
        WHERE geom_3857 && ST_TileEnvelope(:z, :x, :y)
    ) AS tile
""")


@app.get("/tiles/{z}/{x}/{y}.pbf")
def parcel_tile(
    z: int,
    x: int,
    y: int,
    session: Session = Depends(get_session),
):
    """
    Returns a Mapbox Vector Tile containing parcels
    for the requested XYZ tile.
    """

    # Don't generate parcel tiles at extremely low zoom levels.
    if z < 10:
        return Response(
            content=b"",
            media_type="application/vnd.mapbox-vector-tile",
        )

    # Validate XYZ tile coordinates.
    max_tile = 2**z - 1

    if x < 0 or x > max_tile:
        raise HTTPException(
            status_code=400,
            detail="Invalid tile x coordinate.",
        )

    if y < 0 or y > max_tile:
        raise HTTPException(
            status_code=400,
            detail="Invalid tile y coordinate.",
        )

    result = session.execute(
        TILE_SQL,
        {
            "z": z,
            "x": x,
            "y": y,
        },
    ).scalar()

    return Response(
        content=result or b"",
        media_type="application/vnd.mapbox-vector-tile",
        headers={
            "Cache-Control": "public, max-age=3600",
        },
    )


@app.get("/parcel/{prop_id}")
def get_parcel_by_id(
    prop_id: str,
    session: Session = Depends(get_session),
):
    result = get_parcel_by_prop_id(
        session=session,
        prop_id=prop_id,
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail=f"Parcel {prop_id} not found",
        )

    return {
        "prop_id": result.prop_id,
        "area_acres": float(result.area_acres),
        "geometry": json.loads(result.geometry),
    }


@app.post("/map/command")
async def map_command(command: MapCommand):
    if browser_socket is None:
        raise HTTPException(
            status_code=503,
            detail="Map browser is not connected",
        )

    await browser_socket.send_json(command.model_dump())

    return {
        "status": "sent",
        "command": command,
    }


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global browser_socket

    await websocket.accept()

    browser_socket = websocket

    print("Browser connected")

    try:
        while True:
            await websocket.receive_text()

    except Exception:
        browser_socket = None
        print("Browser disconnected")

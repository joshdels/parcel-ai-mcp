from fastapi import Depends, FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.database import get_session

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

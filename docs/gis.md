## optimization inside postgres

The goal is to use 3857 geom tiles that is index by GIST
to achieved faster record

```sql
    --- Creates the table
    ALTER TABLE williamson_parcels
    ADD COLUMN geom_3857 geometry(MultiPolygon, 3857);

    --- Populate it:
    UPDATE williamson_parcels
    SET geom_3857 = ST_Transform(geom, 3857);

    --- Then create the spatial index:
    CREATE INDEX williamson_parcels_geom_3857_idx
    ON williamson_parcels
    USING GIST (geom_3857);
```

This serves the tile into ready gis for the server. As you can see ST_AsMVT converts to thile using geom_3857
ST_TileEnvelope is used to show or render only whats in the map view convered in the boundary

Notes: 
    ST_AsMVT        - converts as tiles
    ST_TileEnvlope  - load only in map boundary

```python
statement = text("""
    SELECT ST_AsMVT(tile, 'williamson_parcels')
    FROM (
        SELECT
            prop_id,
            ST_AsMVTGeom(
                geom_3857,
                ST_TileEnvelope(:z, :x, :y)
            ) AS geom
        FROM williamson_parcels
        WHERE geom_3857 && ST_TileEnvelope(:z, :x, :y)
    ) AS tile
""")
```
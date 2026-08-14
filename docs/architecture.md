# For Tilling Large Data of Postgres to avoid map lagging

```shell
                  HTTP
MapLibre ───────────────────► FastAPI
                               │
                               │ SQLAlchemy
                               ▼
                         PostgreSQL/PostGIS
                               │
                  ST_AsMVT + ST_AsMVTGeom
                               │
                               ▼
                         binary PBF/MVT
                               │
                               ▼
MapLibre ◄─────────────────────┘
```


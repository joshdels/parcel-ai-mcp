# Architecture

this compose of multiple stack

## Techstack

1. UV python
2. Postgres/PostGIS
3. SQL Alchemy
4. MCP SDK python
5. LLM AI Claude
6. FastAPI
7. WebSockets
8. HTML, CSS, JS (front end)

[stack](architecture.png)

## For Tilling Large Data of Postgres to avoid map lagging

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


.PHONY: dev install

dev:
	uv run mcp dev parcel_mcp/server.py

install:
	uv run mcp install parcel_mcp/server.py --with sqlalchemy --with psycopg[binary] --with geoalchemy2 --with fastapi
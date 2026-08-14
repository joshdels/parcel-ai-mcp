.PHONY: dev install api

dev:
	uv run mcp dev parcel_mcp/server.py


mcp:
	uv run mcp install parcel_mcp/server.py \
		--with sqlalchemy \
		--with psycopg[binary] \
		--with geoalchemy2 \
		--with fastapi[standard] \
		--with websockets \
		--with python-dotenv


api:
	uv run fastapi dev app/api/main.py
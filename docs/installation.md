# Getting Started

1. Prepare .env file for the configs

```shell
DB_USER='user name'
DB_PASSWORD='user password'
DB_HOST='host'
DB_DATABASE='database name'

SMTP_USERNAME="<your email>"
SMTP_PASSWORD="<smtp password>"
```

2. Prepare your smtp to send email. 
  Guide is on [here](https://www.youtube.com/watch?v=NEVGgCigW5Q)

3. Ingest parcel data to the postgres, nake it sure postgis extension is created
   Land Parcel Data = [link](https://data.geographic.texas.gov/?s=land%20parcels&pg=1)

4. Optimize postgres/postgis
   Guide is on [here](gis.md)

5. Sync the library dependencies

```shell
uv sync
uv venv
```

```shell
make dev --> testing
make mcp --> install the required mcp server to claude
make api --> to run fast api
```

then open claude desktop to start prompting

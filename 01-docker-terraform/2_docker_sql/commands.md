### Running PostGres with Docker
```bash
docker run -it \
    -e POSTGRES_USER='root' \
    -e POSTGRES_PASSWORD='root' \
    -e POSTGRES_DB='ny_taxi' \
    -v "$(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data" \
    -p 5432:5432 \
    postgres:13
```

### Interacting with Postgres using the CLI
```bash
pgcli -h localhost -p 5432 -U root ny_taxi
```

### Running PGAdmin with Docker (GUI Enviorment)
```bash
docker run -it \
    -e PGADMIN_DEFAULT_EMAIL='admin@admin.com'\
    -e PGADMIN_DEFAULT_PASSWORD='root'\
    -p 8080:80 \
    dpage/pgadmin4
```
### Setting up network for communication between containers
```bash
docker network create pg-network
```

### Running PostGres and PGAdmin with Docker within network
```bash
docker run -it \
    -e POSTGRES_USER='root' \
    -e POSTGRES_PASSWORD='root' \
    -e POSTGRES_DB='ny_taxi' \
    -v "$(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data" \
    -p 5432:5432 \
    --network pg-network \
    --name pg-database \
    postgres:13
```

```bash
docker run -it \
    -e PGADMIN_DEFAULT_EMAIL='admin@admin.com'\
    -e PGADMIN_DEFAULT_PASSWORD='root'\
    -p 8080:80 \
    --network pg-network \
    --name pgadmin-2 \
    dpage/pgadmin4
```

### Running the Ingestion Script
```bash
URL='https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-01.parquet'
ZONES_URL='https://d37ci6vzurychx.cloudfront.net/misc/taxi+_zone_lookup.csv'
python3 ingest-data.py \
    --user=root \
    --password=root \
    --host=localhost \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_trips \
    --url=${URL}
    --zones_url=${ZONES_URL}
```

### Building the Docker Image for the Ingestion Script
```bash
docker build -t taxi_ingest:v001 .
```

### Running the Docker Image
```bash
docker run -it \
    --network pg-network \
    taxi_ingest:v001 \
    --user=root \
    --password=root \
    --host=pg-database \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_trips \
    --url=${URL}
    --zones_url=${ZONES_URL}
```
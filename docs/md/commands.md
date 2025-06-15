pdm init
pdm install
pdm run django-admin startproject src
pdm export -f requirements --without-hashes > requirements.txt
pdm manage migrate
docker-compose up -d --build
pdm run module create v1 auth
pdm manage show_urls
pdm manage seed_users --mode=development
export PATH="$HOME/.local/bin:$PATH
pdm manage seed_users --mode=development --count=100
pdm manage makemigrations places --empty --name enable_postgis_extension
pdm manage makemigrations places
docker-compose down -v
pdm manage seed_places --mode=development --places_per_city=1
pdm manage seed_places_from_csv --mode=development
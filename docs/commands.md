pdm init
pdm install
pdm run django-admin startproject src
pdm export -f requirements --without-hashes > requirements.txt
pdm manage migrate
docker-compose up -d --build
pdm run module create v1 auth
pdm manage show_urls
pdm init
pdm install
pdm run django-admin startproject src
pdm export -f requirements --without-hashes > requirements.txt
pdm manage migrate

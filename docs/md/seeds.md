pdm manage seed_users --mode=development --count=100
pdm manage seed_sensors --mode=development
pdm manage seed_stations --mode=development --stations_per_place=1
pdm manage seed_station_sensors --mode=development
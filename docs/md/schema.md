// ENUMS

Enum Status {
  ACTIVE
  INACTIVE
}

Enum StationStatus {
  ACTIVE
  INACTIVE
  ONLINE
  OFFLINE
  MAINTENANCE
}

Enum PlaceType {
  FARM
  CAMPUS
  CITY
  RESERVE
  OTHER
}

Enum SensorType {
  TEMPERATURE
  HUMIDITY
  WIND
  PRESSURE
  RAINFALL
  OTHER
}

Enum SensorStatus {
  ACTIVE
  INACTIVE
  ERROR
}

Enum MetricType {
  TEMPERATURE
  HUMIDITY
  WIND_SPEED
  WIND_DIRECTION
  PRESSURE
  RAINFALL
  SOLAR_RADIATION
  OTHER
}

Enum AggregationPeriod {
  HOURLY
  DAILY
  WEEKLY
  MONTHLY
}

// ENUMS RELACIONADOS A EVENTOS E LOGS

Enum EventType {
  ALERT
  WARNING
  INFO
  ERROR
}

Enum EventCategory {
  WEATHER       // eventos climáticos
  SENSOR        // falha, status ou calibração de sensor
  SYSTEM        // sistema interno, falhas, atualizações
  MAINTENANCE   // relacionados à manutenção programada ou não
}

Enum EventSeverity {
  LOW
  MEDIUM
  HIGH
  CRITICAL
}

Enum EventStatus {
  OPEN
  ACKNOWLEDGED
  RESOLVED
}

Enum LogSeverity {
  DEBUG
  INFO
  WARN
  ERROR
}

// AUTH & PERMISSIONS

Table users {
  id               integer      [primary key]
  uuid             string       [unique]

  username         string       [unique]
  first_name       string
  last_name        string
  email            string       [unique]
  image            string
  password_hash    string
  status           Status       [default: "ACTIVE"]

  created_at       timestamp
  updated_at       timestamp
}

// e.g. ADMIN, OWNER, MANAGE, OPERATOR, EMPLOYEE, CUSTOMER, VIEWER

Table groups {
  id               integer      [primary key]
  name             string       [unique] 
}

Table user_groups {
  id               integer      [primary key]
  user_id          integer      [ref: > users.id]
  group_id         integer      [ref: > groups.id]
}

Table permissions {
  id               integer      [primary key]
  codename         string       [unique]
  name             string
  content_type     string       // Ex: Sensor, Station, etc.
}

Table group_permissions {
  id               integer      [primary key]
  group_id         integer      [ref: > groups.id]
  permission_id    integer      [ref: > permissions.id]
}

// PLACES & STATIONS

Table places {
  id            integer     [primary key]
  uuid          string      [unique]

  name          string
  description   string
  address       string
  city          string
  state         string
  country       string

  location      point

  status        Status       [default: "ACTIVE"]
  type          PlaceType    [default: "OTHER"]
  user_id       integer      [ref: > users.id]

  created_at    timestamp
  updated_at    timestamp
}

Table stations {
  id                    integer         [primary key]
  uuid                  string          [unique]

  name                  string
  description           string

  model                 string
  firmware              string

  installed_at          timestamp       [null]
  last_maintenance_at   timestamp       [null]
  next_maintenance_at   timestamp       [null]

  battery_level         integer         [null]
  signal_strength       integer         [null]

  status                StationStatus   [default: "ACTIVE"]
  place_id              integer         [ref: > places.id]
  user_id               integer         [ref: > users.id]

  created_at            timestamp
  updated_at            timestamp
}

// SENSORS & DATA

Table sensors {
  id              integer         [primary key]
  uuid            string          [unique]

  type            SensorType
  model           string

  min_value       float
  max_value       float
  calibrated_at   timestamp

  status          SensorStatus    [default: "ACTIVE"]
  station_id      integer         [ref: > stations.id]
  user_id         integer         [ref: > users.id]

  created_at      timestamp
  updated_at      timestamp
}

Table records {
  id              integer         [primary key]
  uuid            string          [unique]

  recorded_at     timestamp
  temperature     float           [null]
  humidity        float           [null]
  wind_speed      float           [null]
  wind_direction  float           [null]
  pressure        float           [null]
  rainfall        float           [null]

  status          Status          [default: "ACTIVE"]
  station_id      integer         [ref: > stations.id]

  created_at      timestamp
  updated_at      timestamp
}

Table sensor_data {
  id              integer         [primary key]
  uuid            string          [unique]

  value           float
  unit            string

  record_id       integer         [ref: > records.id]
  sensor_id       integer         [ref: > sensors.id]

  created_at      timestamp
  updated_at      timestamp
}

// METRIC AGGREGATION (RELATÓRIOS)

Table aggregated_metrics {
  id              integer         [primary key]
  uuid            string          [unique]

  date            date
  metric_type     MetricType
  aggregation     AggregationPeriod

  min_value       float
  max_value       float
  avg_value       float
  sum_value       float
  unit            string

  record_count    integer

  station_id      integer             [ref: > stations.id]
  place_id        integer             [ref: > places.id]
  sensor_id       integer             [ref: > sensors.id, null]

  created_at      timestamp
  updated_at      timestamp
}

Table events {
  id             integer         [primary key]
  uuid           string          [unique]

  title          string
  description    string
  occurred_at    timestamp
  resolved_at    timestamp       [null]

  type           EventType
  category       EventCategory
  severity       EventSeverity
  status         EventStatus     [default: "OPEN"]

  user_id        integer         [ref: > users.id]
  station_id     integer         [ref: > stations.id]
  sensor_id      integer         [ref: > sensors.id, null]

  created_at     timestamp
  updated_at     timestamp
}

Table logs {
  id             integer         [primary key]
  uuid           string          [unique]

  message        string
  level          LogSeverity     [default: "INFO"]

  user_id        integer         [ref: > users.id, null]
  station_id     integer         [ref: > stations.id, null]

  created_at     timestamp
  updated_at     timestamp
}
 


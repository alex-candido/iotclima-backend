CREATE TYPE "Status" AS ENUM (
  'ACTIVE',
  'INACTIVE'
);

CREATE TYPE "StationStatus" AS ENUM (
  'ACTIVE',
  'INACTIVE',
  'ONLINE',
  'OFFLINE',
  'MAINTENANCE'
);

CREATE TYPE "PlaceType" AS ENUM (
  'FARM',
  'CAMPUS',
  'CITY',
  'RESERVE',
  'OTHER'
);

CREATE TYPE "SensorType" AS ENUM (
  'TEMPERATURE',
  'HUMIDITY',
  'WIND',
  'PRESSURE',
  'RAINFALL',
  'OTHER'
);

CREATE TYPE "SensorStatus" AS ENUM (
  'ACTIVE',
  'INACTIVE',
  'ERROR'
);

CREATE TYPE "MetricType" AS ENUM (
  'TEMPERATURE',
  'HUMIDITY',
  'WIND_SPEED',
  'WIND_DIRECTION',
  'PRESSURE',
  'RAINFALL',
  'SOLAR_RADIATION',
  'OTHER'
);

CREATE TYPE "AggregationPeriod" AS ENUM (
  'HOURLY',
  'DAILY',
  'WEEKLY',
  'MONTHLY'
);

CREATE TYPE "EventType" AS ENUM (
  'ALERT',
  'WARNING',
  'INFO',
  'ERROR'
);

CREATE TYPE "EventCategory" AS ENUM (
  'WEATHER',
  'SENSOR',
  'SYSTEM',
  'MAINTENANCE'
);

CREATE TYPE "EventSeverity" AS ENUM (
  'LOW',
  'MEDIUM',
  'HIGH',
  'CRITICAL'
);

CREATE TYPE "EventStatus" AS ENUM (
  'OPEN',
  'ACKNOWLEDGED',
  'RESOLVED'
);

CREATE TYPE "LogSeverity" AS ENUM (
  'DEBUG',
  'INFO',
  'WARN',
  'ERROR'
);

CREATE TABLE "users" (
  "id" integer PRIMARY KEY,
  "uuid" string UNIQUE,
  "username" string UNIQUE,
  "first_name" string,
  "last_name" string,
  "email" string UNIQUE,
  "image" string,
  "password_hash" string,
  "status" Status DEFAULT 'ACTIVE',
  "created_at" timestamp,
  "updated_at" timestamp
);

CREATE TABLE "groups" (
  "id" integer PRIMARY KEY,
  "name" string UNIQUE
);

CREATE TABLE "user_groups" (
  "id" integer PRIMARY KEY,
  "user_id" integer,
  "group_id" integer
);

CREATE TABLE "permissions" (
  "id" integer PRIMARY KEY,
  "codename" string UNIQUE,
  "name" string,
  "content_type" string
);

CREATE TABLE "group_permissions" (
  "id" integer PRIMARY KEY,
  "group_id" integer,
  "permission_id" integer
);

CREATE TABLE "places" (
  "id" integer PRIMARY KEY,
  "uuid" string UNIQUE,
  "name" string,
  "description" string,
  "address" string,
  "city" string,
  "state" string,
  "country" string,
  "location" point,
  "status" Status DEFAULT 'ACTIVE',
  "type" PlaceType DEFAULT 'OTHER',
  "user_id" integer,
  "created_at" timestamp,
  "updated_at" timestamp
);

CREATE TABLE "stations" (
  "id" integer PRIMARY KEY,
  "uuid" string UNIQUE,
  "name" string,
  "description" string,
  "model" string,
  "firmware" string,
  "installed_at" timestamp,
  "last_maintenance_at" timestamp,
  "next_maintenance_at" timestamp,
  "battery_level" integer,
  "signal_strength" integer,
  "status" StationStatus DEFAULT 'ACTIVE',
  "place_id" integer,
  "user_id" integer,
  "created_at" timestamp,
  "updated_at" timestamp
);

CREATE TABLE "sensors" (
  "id" integer PRIMARY KEY,
  "uuid" string UNIQUE,
  "type" SensorType,
  "model" string,
  "min_value" float,
  "max_value" float,
  "calibrated_at" timestamp,
  "status" SensorStatus DEFAULT 'ACTIVE',
  "station_id" integer,
  "user_id" integer,
  "created_at" timestamp,
  "updated_at" timestamp
);

CREATE TABLE "records" (
  "id" integer PRIMARY KEY,
  "uuid" string UNIQUE,
  "recorded_at" timestamp,
  "temperature" float,
  "humidity" float,
  "wind_speed" float,
  "wind_direction" float,
  "pressure" float,
  "rainfall" float,
  "status" Status DEFAULT 'ACTIVE',
  "station_id" integer,
  "created_at" timestamp,
  "updated_at" timestamp
);

CREATE TABLE "sensor_data" (
  "id" integer PRIMARY KEY,
  "uuid" string UNIQUE,
  "value" float,
  "unit" string,
  "record_id" integer,
  "sensor_id" integer,
  "created_at" timestamp,
  "updated_at" timestamp
);

CREATE TABLE "aggregated_metrics" (
  "id" integer PRIMARY KEY,
  "uuid" string UNIQUE,
  "date" date,
  "metric_type" MetricType,
  "aggregation" AggregationPeriod,
  "min_value" float,
  "max_value" float,
  "avg_value" float,
  "sum_value" float,
  "unit" string,
  "record_count" integer,
  "station_id" integer,
  "place_id" integer,
  "sensor_id" integer,
  "created_at" timestamp,
  "updated_at" timestamp
);

CREATE TABLE "events" (
  "id" integer PRIMARY KEY,
  "uuid" string UNIQUE,
  "title" string,
  "description" string,
  "occurred_at" timestamp,
  "resolved_at" timestamp,
  "type" EventType,
  "category" EventCategory,
  "severity" EventSeverity,
  "status" EventStatus DEFAULT 'OPEN',
  "user_id" integer,
  "station_id" integer,
  "sensor_id" integer,
  "created_at" timestamp,
  "updated_at" timestamp
);

CREATE TABLE "logs" (
  "id" integer PRIMARY KEY,
  "uuid" string UNIQUE,
  "message" string,
  "level" LogSeverity DEFAULT 'INFO',
  "user_id" integer,
  "station_id" integer,
  "created_at" timestamp,
  "updated_at" timestamp
);

ALTER TABLE "user_groups" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "user_groups" ADD FOREIGN KEY ("group_id") REFERENCES "groups" ("id");

ALTER TABLE "group_permissions" ADD FOREIGN KEY ("group_id") REFERENCES "groups" ("id");

ALTER TABLE "group_permissions" ADD FOREIGN KEY ("permission_id") REFERENCES "permissions" ("id");

ALTER TABLE "places" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "stations" ADD FOREIGN KEY ("place_id") REFERENCES "places" ("id");

ALTER TABLE "stations" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "sensors" ADD FOREIGN KEY ("station_id") REFERENCES "stations" ("id");

ALTER TABLE "sensors" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "records" ADD FOREIGN KEY ("station_id") REFERENCES "stations" ("id");

ALTER TABLE "sensor_data" ADD FOREIGN KEY ("record_id") REFERENCES "records" ("id");

ALTER TABLE "sensor_data" ADD FOREIGN KEY ("sensor_id") REFERENCES "sensors" ("id");

ALTER TABLE "aggregated_metrics" ADD FOREIGN KEY ("station_id") REFERENCES "stations" ("id");

ALTER TABLE "aggregated_metrics" ADD FOREIGN KEY ("place_id") REFERENCES "places" ("id");

ALTER TABLE "aggregated_metrics" ADD FOREIGN KEY ("sensor_id") REFERENCES "sensors" ("id");

ALTER TABLE "events" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "events" ADD FOREIGN KEY ("station_id") REFERENCES "stations" ("id");

ALTER TABLE "events" ADD FOREIGN KEY ("sensor_id") REFERENCES "sensors" ("id");

ALTER TABLE "logs" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "logs" ADD FOREIGN KEY ("station_id") REFERENCES "stations" ("id");

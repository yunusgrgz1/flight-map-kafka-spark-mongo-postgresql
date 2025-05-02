CREATE TABLE flights (
    id serial primary key ,
    flight_id integer unique,
    airline VARCHAR(100),
    flight_status VARCHAR(50),
    departure_city VARCHAR(100),
    departure_airport VARCHAR(100),
    arrival_city VARCHAR(100),
    arrival_airport VARCHAR(100),
    scheduled_departure_time TIMESTAMP,
    actual_departure_time TIMESTAMP,
    scheduled_arrival_time TIMESTAMP,
    actual_landed_time TIMESTAMP,
    delayed_status
);


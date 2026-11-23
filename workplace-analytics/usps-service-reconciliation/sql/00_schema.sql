-- PUBLIC RECONSTRUCTION / invented names and records only. SQLite 3.25+
PRAGMA foreign_keys=ON;
CREATE TABLE orders (
  load_id TEXT PRIMARY KEY, trip_id TEXT NOT NULL, lane TEXT NOT NULL, carrier TEXT NOT NULL,
  origin_sched_departure TEXT NOT NULL, origin_actual_departure TEXT,
  destination_sched_arrival TEXT NOT NULL, destination_actual_arrival TEXT
);
CREATE TABLE usps_events (
  event_id TEXT PRIMARY KEY, load_id TEXT NOT NULL, event_type TEXT NOT NULL
    CHECK(event_type IN ('departure','arrival')),
  scheduled_at TEXT NOT NULL, actual_at TEXT, lane TEXT NOT NULL,
  FOREIGN KEY(load_id) REFERENCES orders(load_id)
);
CREATE TABLE adjudications (
  case_id TEXT PRIMARY KEY, load_id TEXT NOT NULL,
  event_type TEXT CHECK(event_type IN ('departure','arrival')),
  scheduled_at TEXT, decision TEXT NOT NULL CHECK(decision IN ('approved','pending','denied'))
);
CREATE TABLE lane_benchmarks (
  lane TEXT PRIMARY KEY, reported_departure_rate REAL, reported_arrival_rate REAL,
  reported_departure_events INTEGER, reported_arrival_events INTEGER
);
CREATE INDEX idx_events_load_type ON usps_events(load_id,event_type,scheduled_at);
CREATE INDEX idx_cases_match ON adjudications(load_id,event_type,scheduled_at,decision);

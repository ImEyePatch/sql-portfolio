-- Independent synthetic model based on the categories documented in an internal BI report.
CREATE TABLE loads (
 load_id TEXT PRIMARY KEY, carrier TEXT NOT NULL, lane TEXT NOT NULL,
 departed_at TEXT, expected_stops INTEGER NOT NULL CHECK(expected_stops>=0)
);
CREATE TABLE weekly_snapshots (
 snapshot_id TEXT PRIMARY KEY, load_id TEXT NOT NULL REFERENCES loads(load_id),
 week_start TEXT NOT NULL, ping_interval_min INTEGER,
 geofence_stops_detected INTEGER, geofence_stops_expected INTEGER NOT NULL,
 has_movement INTEGER NOT NULL CHECK(has_movement IN (0,1)),
 CHECK(geofence_stops_expected>=0),
 CHECK(geofence_stops_detected IS NULL OR geofence_stops_detected>=0)
);
CREATE TABLE geofence_events (
 id TEXT PRIMARY KEY, load_id TEXT NOT NULL REFERENCES loads(load_id),
 facility TEXT NOT NULL, event_type TEXT CHECK(event_type IN ('arrival','departure')),
 event_at TEXT, appointment_at TEXT
);
CREATE INDEX idx_weekly_scope ON weekly_snapshots(week_start,load_id);

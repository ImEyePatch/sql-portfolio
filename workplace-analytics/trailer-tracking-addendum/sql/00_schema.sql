-- Synthetic supplement to the pre-existing trailer tracking public portfolio.
CREATE TABLE assets(asset_id TEXT PRIMARY KEY, provider TEXT NOT NULL);
CREATE TABLE tracking_events (
 event_id TEXT PRIMARY KEY,asset_id TEXT NOT NULL REFERENCES assets(asset_id),
 event_at TEXT NOT NULL,city TEXT,region TEXT,motion_status TEXT NOT NULL,
 speed_mph REAL, idle_hours REAL NOT NULL DEFAULT 0
);
CREATE TABLE trip_orders (
 order_id TEXT PRIMARY KEY,asset_id TEXT NOT NULL REFERENCES assets(asset_id),
 departed_at TEXT, arrived_at TEXT, expected_return_at TEXT,
 carrier TEXT,route TEXT, movement_status TEXT
);
CREATE TABLE approved_hubs (city TEXT NOT NULL,region TEXT NOT NULL,PRIMARY KEY(city,region));
CREATE INDEX idx_tracking_latest ON tracking_events(asset_id,event_at);
CREATE INDEX idx_order_asset_departed ON trip_orders(asset_id,departed_at);

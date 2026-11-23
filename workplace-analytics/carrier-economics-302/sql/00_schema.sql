-- Synthetic-only carrier cost and trip timing schema.
CREATE TABLE orders (
 order_id TEXT PRIMARY KEY, carrier TEXT NOT NULL, lane TEXT NOT NULL,
 scheduled_arrival TEXT, actual_arrival TEXT,
 revenue REAL NOT NULL, base_carrier_cost REAL NOT NULL, trip_id TEXT
);
CREATE TABLE trips (
 trip_id TEXT PRIMARY KEY, trip_lane TEXT, miles REAL, planned_drive_hours REAL,
 actual_drive_hours REAL
);
CREATE TABLE driver_extra_pay (
 pay_id TEXT PRIMARY KEY, order_id TEXT NOT NULL REFERENCES orders(order_id),
 pay_code TEXT NOT NULL, amount REAL NOT NULL
);
CREATE TABLE rate_confirmations (
 confirmation_id TEXT PRIMARY KEY, order_id TEXT NOT NULL REFERENCES orders(order_id),
 issued_at TEXT NOT NULL, acknowledged_at TEXT
);
CREATE INDEX idx_driver_pay_order ON driver_extra_pay(order_id);
CREATE INDEX idx_rate_order ON rate_confirmations(order_id);

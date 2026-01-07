import requests
import pandas as pd
import time
from datetime import datetime, timezone
from pathlib import Path
from collections import deque

API_KEYS = [
    "eyJvcmciOiI2MmY2YTYxZDgyODM5ZjAwMDE4NmExY2EiLCJpZCI6IjRhYWZkNTY3NTA5YjRlOGU5OWJjZDVmMmQ0MGYyOTJiIiwiaCI6Im11cm11cjEyOCJ9",
    "eyJvcmciOiI2MmY2YTYxZDgyODM5ZjAwMDE4NmExY2EiLCJpZCI6IjJiZGViYTFhZmE5ZjRjMzdhMzQzMTkyNzE5MzhlNjQ3IiwiaCI6Im11cm11cjEyOCJ9",
]

BASE_URL = "https://api.mcleodsoftware.com/mpact-sandbox/rates"

LANES = [
    ("900", "606"), ("606", "900"), ("100", "606"), ("606", "100"), ("900", "100"),
    ("100", "900"), ("900", "750"), ("750", "900"), ("900", "770"), ("770", "900"),
    ("606", "750"), ("750", "606"), ("606", "770"), ("770", "606"), ("100", "303"),
    ("303", "100"), ("303", "750"), ("750", "303"), ("303", "770"), ("770", "303"),
    ("750", "770"), ("770", "750"), ("606", "303"), ("303", "606"), ("100", "770"),
    ("770", "100"), ("750", "100"), ("100", "750"), ("900", "981"), ("981", "900"),
    ("606", "981"), ("981", "606"), ("100", "981"), ("981", "100"), ("303", "981"),
    ("981", "303"), ("750", "981"), ("981", "750"), ("770", "981"), ("981", "770"),
    ("331", "100"), ("100", "331"), ("331", "606"), ("606", "331"), ("331", "303"),
    ("303", "331"), ("331", "750"), ("750", "331"), ("331", "770"), ("770", "331"),
    ("191", "100"), ("100", "191"), ("191", "606"), ("606", "191"), ("191", "303"),
    ("303", "191"), ("850", "900"), ("900", "850"), ("850", "750"), ("750", "850"),
    ("850", "606"), ("606", "850"), ("850", "303"), ("303", "850"), ("381", "606"),
    ("606", "381"), ("381", "303"), ("303", "381"), ("941", "900"), ("900", "941"),
    ("941", "606"), ("606", "941"), ("482", "606"), ("606", "482"), ("021", "100"),
    ("100", "021"), ("802", "750"), ("750", "802"), ("802", "606"), ("606", "802"),
    ("554", "606"), ("606", "554"), ("462", "606"), ("606", "462"), ("282", "303"),
    ("303", "282"), ("641", "750"), ("750", "641"), ("432", "303"), ("303", "432"),
    ("212", "100"), ("100", "212"), ("972", "981"), ("981", "972"), ("372", "303"),
    ("303", "372"), ("441", "606"), ("606", "441"), ("336", "331"), ("331", "336"),
]

TRAILER_TYPES = ["Van", "Flatbed", "Reefer"]
CARRIER_TYPE_SELL = "Asset"
CARRIER_TYPE_BUY = "Broker"
OUTPUT_FILE = Path("mpact_rates.csv")

MAX_REQUESTS_PER_MIN = 200
MAX_REQUESTS_PER_KEY = 700
BATCH_SIZE = 25
RETRY_LIMIT = 3

request_counters = {key: 0 for key in API_KEYS}
key_usage_timestamps = {key: deque(maxlen=MAX_REQUESTS_PER_MIN) for key in API_KEYS}


def get_next_available_key():
    """Get next API key that hasn't exhausted its quota"""
    for i, key in enumerate(API_KEYS):
        if request_counters[key] < MAX_REQUESTS_PER_KEY:
            return key, i
    return None, None


def fetch(endpoint_type, params):
    """Fetch data from API with key rotation and rate limiting"""
    url = f"{BASE_URL}/{endpoint_type}"
    retries = 0
    
    while retries <= RETRY_LIMIT:
        current_key, key_index = get_next_available_key()
        if current_key is None:
            raise RuntimeError("All API keys have exhausted their quota")
        
        now = time.time()
        while (key_usage_timestamps[current_key] and 
                now - key_usage_timestamps[current_key][0] > 60):
            key_usage_timestamps[current_key].popleft()
        
        if len(key_usage_timestamps[current_key]) >= MAX_REQUESTS_PER_MIN:
            wait_time = 60 - (now - key_usage_timestamps[current_key][0])
            print(f"Key {key_index} rate limited. Waiting {wait_time:.1f}s...")
            time.sleep(wait_time)
            continue
        
        headers = {
            "Accept": "application/json",
            "X-Api-Key": current_key,
        }

        try:
            resp = requests.get(url, headers=headers, params=params, timeout=15)

            if resp.status_code == 429:
                print(f"[429] Rate limit hit for key {key_index}. Will try another key on retry...")
                retries += 1
                time.sleep(2 ** retries)
                continue

            if resp.status_code in {401, 403}:
                print(f"[{resp.status_code}] Auth error with key {key_index}. Marking as exhausted.")
                request_counters[current_key] = MAX_REQUESTS_PER_KEY 
                retries += 1
                time.sleep(2 ** retries)
                continue

            resp.raise_for_status()
            
            request_counters[current_key] += 1
            key_usage_timestamps[current_key].append(time.time())
            
            if request_counters[current_key] >= MAX_REQUESTS_PER_KEY:
                print(f"Key {key_index} exhausted ({request_counters[current_key]}/{MAX_REQUESTS_PER_KEY}).")
            
            return resp.json()

        except Exception as e:
            print(f"[Error] Attempt {retries + 1} failed with key {key_index}: {e}")
            retries += 1
            time.sleep(2 ** retries)

    raise RuntimeError(f"Failed after {RETRY_LIMIT} retries for {params}")


def row_from_payload(endpoint_type, origin_zip, dest_zip, trailer, carrier, include_fuel, include_quartiles, payload):
    """Create a data row from API payload"""
    src = payload.get("sourceInfo", {}) or {}
    return {
        "pulled_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "endpoint_type": endpoint_type,
        "origin_zip3": origin_zip,
        "destination_zip3": dest_zip,
        "trailer_type": trailer,
        "carrier_type": carrier,
        "include_fuel": include_fuel,
        "include_quartiles": include_quartiles,
        "average": payload.get("average"),
        "minimum": payload.get("minimum"),
        "maximum": payload.get("maximum"),
        "quartile1": payload.get("quartile1"),
        "quartile2": payload.get("quartile2"),
        "quartile3": payload.get("quartile3"),
        "orders": src.get("orders"),
        "contributors": src.get("contributors"),
        "days_window": src.get("days"),
    }


def main():
    """Main execution function"""
    if OUTPUT_FILE.exists():
        try:
            completed_df = pd.read_csv(OUTPUT_FILE, usecols=[
                "origin_zip3", "destination_zip3", "trailer_type", 
                "carrier_type", "endpoint_type", "include_fuel"
            ])
            completed = {
                (row.origin_zip3, row.destination_zip3, row.trailer_type, 
                    row.carrier_type, row.endpoint_type, row.include_fuel)
                for row in completed_df.itertuples(index=False)
            }
            print(f"Found {len(completed)} previously completed tasks in CSV.")
        except Exception as e:
            print(f"Error reading existing CSV: {e}. Starting fresh.")
            completed = set()
            pd.DataFrame(columns=[
                "pulled_at", "endpoint_type", "origin_zip3", "destination_zip3", "trailer_type",
                "carrier_type", "include_fuel", "include_quartiles", "average", "minimum", "maximum",
                "quartile1", "quartile2", "quartile3", "orders", "contributors", "days_window"
            ]).to_csv(OUTPUT_FILE, index=False)
    else:
        completed = set()
        pd.DataFrame(columns=[
            "pulled_at", "endpoint_type", "origin_zip3", "destination_zip3", "trailer_type",
            "carrier_type", "include_fuel", "include_quartiles", "average", "minimum", "maximum",
            "quartile1", "quartile2", "quartile3", "orders", "contributors", "days_window"
        ]).to_csv(OUTPUT_FILE, index=False)

    queue = deque()
    total_requests_needed = 0
    include_quartiles = True

    for origin, dest in LANES:
        for trailer in TRAILER_TYPES:
            for endpoint, carrier in [("buy", CARRIER_TYPE_BUY), ("sell", CARRIER_TYPE_SELL)]:
                for fuel in [True, False]: 
                    signature = (origin, dest, trailer, carrier, endpoint, fuel)
                    if signature in completed:
                        continue
                    queue.append({
                        "origin": origin,
                        "dest": dest,
                        "trailer": trailer,
                        "endpoint": endpoint,
                        "carrier": carrier,
                        "include_fuel": fuel
                    })
                    total_requests_needed += 1

    print(f"Starting batch processing of {len(queue)} queued requests.")
    print(f"Total unique requests needed: {total_requests_needed}")
    print(f"Available API keys: {len(API_KEYS)} (700 requests each)")
    
    failed = []
    processed_count = 0
    start_time = time.time()

    while queue:
        available_key, _ = get_next_available_key()
        if available_key is None:
            print("All API keys have exhausted their quota. Stopping.")
            break
        
        batch_size = min(BATCH_SIZE, len(queue))
        batch = [queue.popleft() for _ in range(batch_size)]

        for task in batch:
            signature = (
                task["origin"], task["dest"], task["trailer"], 
                task["carrier"], task["endpoint"], task["include_fuel"]
            )
            if signature in completed:
                print(f"Skipping already completed: {signature}")
                continue

            params = {
                "originZip": task["origin"],
                "destinationZip": task["dest"],
                "trailerType": task["trailer"],
                "carrierType": task["carrier"],
                "includeFuel": str(task["include_fuel"]).lower(),
                "includeQuartiles": str(include_quartiles).lower(),
            }

            try:
                payload = fetch(task["endpoint"], params)
                row = row_from_payload(
                    task["endpoint"], task["origin"], task["dest"], 
                    task["trailer"], task["carrier"], task["include_fuel"], 
                    include_quartiles, payload
                )
                pd.DataFrame([row]).to_csv(OUTPUT_FILE, mode='a', header=False, index=False)
                
                completed.add(signature)
                processed_count += 1
                
                print(f"[{processed_count}] {task['origin']}→{task['dest']} | "
                        f"{task['trailer']} | {task['endpoint'].upper()} | "
                        f"Fuel: {task['include_fuel']}")
                
            except Exception as e:
                print(f"[Retry Queue] {task['origin']}→{task['dest']} | "
                        f"{task['trailer']} | {task['endpoint'].upper()} failed: {e}")
                failed.append(task)

        print(f"📊 Progress: {processed_count}/{total_requests_needed} | "
                f"Queue: {len(queue)} | Failed: {len(failed)} | "
                f"Key usage: {request_counters}")
        
        time.sleep(0.5)

    if failed:
        print(f"Retrying {len(failed)} failed requests...")
        queue.extend(failed)
        failed.clear()
        
        while queue:
            available_key, _ = get_next_available_key()
            if available_key is None:
                print("All keys exhausted during retry. Stopping.")
                break
                
            task = queue.popleft()
            signature = (
                task["origin"], task["dest"], task["trailer"], 
                task["carrier"], task["endpoint"], task["include_fuel"]
            )
            
            if signature in completed:
                continue
                
            try:
                params = {
                    "originZip": task["origin"],
                    "destinationZip": task["dest"],
                    "trailerType": task["trailer"],
                    "carrierType": task["carrier"],
                    "includeFuel": str(task["include_fuel"]).lower(),
                    "includeQuartiles": str(include_quartiles).lower(),
                }
                
                payload = fetch(task["endpoint"], params)
                row = row_from_payload(
                    task["endpoint"], task["origin"], task["dest"], 
                    task["trailer"], task["carrier"], task["include_fuel"], 
                    include_quartiles, payload
                )
                pd.DataFrame([row]).to_csv(OUTPUT_FILE, mode='a', header=False, index=False)
                
                completed.add(signature)
                processed_count += 1
                print(f"[RETRY] {task['origin']}→{task['dest']} | "
                        f"{task['trailer']} | {task['endpoint'].upper()}")
                
            except Exception as e:
                print(f"Permanent failure: {task['origin']}→{task['dest']} | "
                        f"{task['trailer']}: {e}")

    elapsed_time = time.time() - start_time
    print(f"\nProcessing complete!")
    print(f"Total time: {elapsed_time:.1f}s")
    print(f"Total processed: {processed_count}/{total_requests_needed}")
    print(f"Key usage summary:")
    for i, key in enumerate(API_KEYS):
        print(f"   Key {i}: {request_counters[key]}/{MAX_REQUESTS_PER_KEY} requests")
    print(f"Data saved to: {OUTPUT_FILE.absolute()}")
    
    input("\nPress [Enter] to exit...")


if __name__ == "__main__":
    main()
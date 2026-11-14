import time
import random
import sys

# 1. Generate Timetable Data Function
def generate_timetable(num_trains):
    """Generates a nested timetable dictionary for a given number of trains."""
    stations_pool = ["SBC", "YPR", "DMM", "MAS", "TPTY", "CBE", "MDU", "SCT"]
    days_pool = [
        {"Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"}, 
        {"Mon", "Wed", "Fri"}, 
        {"Tue", "Thu", "Sat"},
        {"Sun"}
    ]
    
    timetable = {}
    for i in range(1, num_trains + 1):
        train_no = str(12600 + i)
        num_stops = random.randint(3, 8)
        stops = []
        for _ in range(num_stops):
            st_code = random.choice(stations_pool)
            arr = f"{random.randint(0,23):02d}:{random.randint(0,59):02d}"
            dep = f"{random.randint(0,23):02d}:{random.randint(0,59):02d}"
            stops.append((st_code, arr, dep))
            
        timetable[train_no] = {
            "name": f"Express Train {i}",
            "stops": stops,
            "days": random.choice(days_pool)
        }
    return timetable

# 2. Build Inverted Station Index
def build_station_index(timetable):
    """Builds an index mapping each station code to a list of train numbers passing through it."""
    station_index = {}
    for train_no, info in timetable.items():
        for station, arr, dep in info["stops"]:
            station_index.setdefault(station, []).append(train_no)
    return station_index

# 3. Query Without Index (Linear Scan)
def query_without_index(timetable, target_station, target_day):
    results = []
    for train_no, info in timetable.items():
        if target_day in info["days"]:
            for station, arr, dep in info["stops"]:
                if station == target_station:
                    results.append((train_no, info["name"], arr, dep))
    return results

# 4. Query With Station Index (Optimized Lookup)
def query_with_index(timetable, station_index, target_station, target_day):
    results = []
    train_list = station_index.get(target_station, [])
    for train_no in train_list:
        info = timetable[train_no]
        if target_day in info["days"]:
            for station, arr, dep in info["stops"]:
                if station == target_station:
                    results.append((train_no, info["name"], arr, dep))
    return results

if __name__ == "__main__":
    # Test with 1,000 trains
    print("--- Generating Timetable Data ---")
    timetable_data = generate_timetable(1000)
    station_index = build_station_index(timetable_data)
    
    target_station = "SBC"
    target_day = "Mon"
    
    # Experimental Investigation & Timing
    print(f"\nSearching for trains at station '{target_station}' running on '{target_day}':")
    
    # Without Index
    start_time = time.time()
    res_no_idx = query_without_index(timetable_data, target_station, target_day)
    time_no_idx = time.time() - start_time
    
    # With Index
    start_time = time.time()
    res_with_idx = query_with_index(timetable_data, station_index, target_station, target_day)
    time_with_idx = time.time() - start_time
    
    print(f"Results found (No Index): {len(res_no_idx)} trains | Time: {time_no_idx:.6f} seconds")
    print(f"Results found (With Index): {len(res_with_idx)} trains | Time: {time_with_idx:.6f} seconds")
    
    # Memory Measurement
    index_memory = sys.getsizeof(station_index)
    print(f"\nExtra memory consumed by station index: {index_memory} bytes")
    
    # Test with Unknown Station / Non-running day
    print("\nTesting edge cases:")
    print("Unknown Station Query:", query_with_index(timetable_data, station_index, "XYZ", "Mon"))
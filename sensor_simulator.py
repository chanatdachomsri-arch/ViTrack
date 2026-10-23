
import random
import time
from datetime import datetime

def generate_sensor_data():
    """Generate simulated ViTrack sensor readings."""
    return {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "ppg_bpm": random.randint(65, 100),
        "fsr_raw": random.randint(100, 900),
        "ntc_temp_c": round(random.uniform(35.5, 37.5), 1),
    }

if __name__ == "__main__":
    while True:
        data = generate_sensor_data()
        print(data)
        time.sleep(2)
import time
from CreaTeBME import SensorManager
from collections import deque

# Create a sensor manager for the given sensor names using the given callback
manager = SensorManager(['890E'])

# Create deque objects to store the sensor measurements and timestamps with a maximum length of 500
timestamps = deque(maxlen=500)
sensor_data = deque(maxlen=500)

# Initialize variables for sampling frequency calculation
start_time = None
sample_count = 0
measurement_count = 0
sampling_frequency_sum = 0

# Start the sensor manager
manager.start()

while True:
    measurements = manager.get_measurements()

    for sensor, data in measurements.items():
        if len(data) > 0:  # Ensure data has at least 6 values
            for chunk in data:
                timestamp = time.time()  # Record the current timestamp
                timestamps.append(timestamp)
                sensor_data.append(chunk)

                # Calculate sampling frequency for every 1 second of data
                if start_time is None:
                    start_time = timestamp
                elif timestamp - start_time >= 1.0:
                    sample_count += 1
                    elapsed_time = timestamp - start_time
                    sampling_frequency = sample_count / elapsed_time
                    sampling_frequency_sum += sampling_frequency
                    start_time = timestamp
                    sample_count = 0
                    measurement_count += 1

                sample_count += 1

                # Calculate average sampling frequency every 30 measurements
                if measurement_count >= 30:
                    average_sampling_frequency = sampling_frequency_sum / measurement_count
                    print("Average Sampling Frequency:", average_sampling_frequency)
                    measurement_count = 0
                    sampling_frequency_sum = 0

# Stop the sensor manager
manager.stop()
# average sampling fequency for 890E is 101 Hz
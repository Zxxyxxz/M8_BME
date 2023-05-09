import time
from CreaTeBME import SensorManager

# Create a sensor manager for the given sensor names using the given callback
# manager = SensorManager(['890E'])
manager = SensorManager(['890E','7516'])


# Start the sensor manager
manager.start()
# manager_2.start()
while True:
    measurements = manager.get_measurements()

    for sensor, data in measurements.items():
        if not data: continue
        if len(data) > 0:
            print(sensor, data)

# Stop the sensor manager
manager.stop()
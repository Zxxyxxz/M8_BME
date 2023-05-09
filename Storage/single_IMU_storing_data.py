import time
from CreaTeBME import SensorManager

# Create a sensor manager for the given sensor names using the given callback
manager = SensorManager(['890E'])

# Create empty lists to store the sensor measurements
acc_x = []
acc_y = []
acc_z = []
gyro_x = []
gyro_y = []
gyro_z = []

# Start the sensor manager
manager.start()

while True:
    measurements = manager.get_measurements()

    for sensor, data in measurements.items():
        if not data:
            continue
        if len(data) > 0 :  # Ensure data has at least 6 values
            if sensor == '890E':
                print(sensor, data)
                print(data[0])
                print(data[1])

                # Extract accelerometer and gyroscope values from each chunk
                for chunk in data:
                    acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z = chunk
                    acc_x.append(acc_x)  # Store accelerometer x
                    acc_y.append(acc_y)  # Store accelerometer y
                    acc_z.append(acc_z)  # Store accelerometer z
                    gyro_x.append(gyro_x)  # Store gyroscope x
                    gyro_y.append(gyro_y)  # Store gyroscope y
                    gyro_z.append(gyro_z)  # Store gyroscope z

    # Continue with the rest of your code or processing logic

# Stop the sensor manager
manager.stop()

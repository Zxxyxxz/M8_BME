import time
from CreaTeBME import SensorManager

# Create a sensor manager for the given sensor names using the given callback
manager = SensorManager(['890E', '7516'])

# Create empty lists to store the sensor measurements for each IMU
acc_x_890E = []
acc_y_890E = []
acc_z_890E = []
gyro_x_890E = []
gyro_y_890E = []
gyro_z_890E = []

acc_x_7516 = []
acc_y_7516 = []
acc_z_7516 = []
gyro_x_7516 = []
gyro_y_7516 = []
gyro_z_7516 = []

# Start the sensor manager
manager.start()

while True:
    measurements = manager.get_measurements()

    for sensor, data in measurements.items():
        if not data:
            continue
        if len(data) > 0:  # Ensure data has at least 6 values
            if sensor == '890E':

                # if len(data) > 2:
                    # print(data[0])
                    # print(data[1])

                # Extract accelerometer and gyroscope values from each chunk
                for chunk in data:
                    acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z = chunk
                    acc_x_890E.append(acc_x)  # Store accelerometer x for IMU 890E
                    acc_y_890E.append(acc_y)  # Store accelerometer y for IMU 890E
                    acc_z_890E.append(acc_z)  # Store accelerometer z for IMU 890E
                    gyro_x_890E.append(gyro_x)  # Store gyroscope x for IMU 890E
                    gyro_y_890E.append(gyro_y)  # Store gyroscope y for IMU 890E
                    gyro_z_890E.append(gyro_z)  # Store gyroscope z for IMU 890E

            elif sensor == '7516':
                # print(sensor, data)
                # if len(data) > 2:
                    # print(data[0])
                    # print(data[1])

                # Extract accelerometer and gyroscope values from each chunk
                for chunk in data:
                    acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z = chunk
                    acc_x_7516.append(acc_x)  # Store accelerometer x for IMU 7516
                    acc_y_7516.append(acc_y)  # Store accelerometer y for IMU 7516
                    acc_z_7516.append(acc_z)  # Store accelerometer z for IMU 7516
                    gyro_x_7516.append(gyro_x)  # Store gyroscope x for IMU 7516
                    gyro_y_7516.append(gyro_y)  # Store gyroscope y for IMU 7516
                    gyro_z_7516.append(gyro_z)  # Store gyroscope z for IMU 7516
            print(sensor,data)
            print(acc_x_890E)
            print(acc_x_7516)
    # Continue with the rest of your code or processing logic

# Stop the sensor manager
manager.stop()



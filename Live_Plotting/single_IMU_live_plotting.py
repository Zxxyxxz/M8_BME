import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from CreaTeBME import SensorManager
from collections import deque

# Define the figure and axis using subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6))

# Create a sensor manager for the given sensor names using the given callback
manager = SensorManager(['890E'])

# Create deque objects to store the sensor measurements and timestamps with a maximum length of 500
# deque supports setting a maximum length for the queue. When the queue reaches the maximum length, adding
# new elements to one end will automatically remove elements from the other end.
timestamps = deque(maxlen=500)
sensor_890E_acc_x = deque(maxlen=500)
sensor_890E_acc_y = deque(maxlen=500)
sensor_890E_acc_z = deque(maxlen=500)
sensor_890E_gyro_x = deque(maxlen=500)
sensor_890E_gyro_y = deque(maxlen=500)
sensor_890E_gyro_z = deque(maxlen=500)

# Animation update function
def animate(i):
    measurements = manager.get_measurements()

    for sensor, data in measurements.items():
        if not data:
            continue
        if len(data) > 0:  # Ensure data has at least 6 values
            if sensor == '890E':
                timestamp = time.time()  # Record the current timestamp
                timestamps.append(timestamp)
                print(sensor, data)
                print(data[0])

                # Extract accelerometer and gyroscope values from each chunk
                for chunk in data:
                    acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z = chunk
                    sensor_890E_acc_x.append(acc_x)  # Store accelerometer x
                    sensor_890E_acc_y.append(acc_y)  # Store accelerometer y
                    sensor_890E_acc_z.append(acc_z)  # Store accelerometer z
                    sensor_890E_gyro_x.append(gyro_x)  # Store gyroscope x
                    sensor_890E_gyro_y.append(gyro_y)  # Store gyroscope y
                    sensor_890E_gyro_z.append(gyro_z)  # Store gyroscope z
                print("######################################################################3####")
                print(sensor_890E_acc_x)

                print("______________________________________________________________________________")

    ax1.clear()
    if timestamps and sensor_890E_acc_x and sensor_890E_acc_y and sensor_890E_acc_z:
        ax1.plot(sensor_890E_acc_x, label='ACC X')
        ax1.plot(sensor_890E_acc_y, label='ACC Y')
        ax1.plot(sensor_890E_acc_z, label='ACC Z')
        ax1.set_title('Sensor 890E - Accelerometer')
        ax1.legend()

    ax2.clear()
    if timestamps and sensor_890E_gyro_x and sensor_890E_gyro_y and sensor_890E_gyro_z:
        ax2.plot(sensor_890E_gyro_x, label='GYRO X')
        ax2.plot(sensor_890E_gyro_y, label='GYRO Y')
        ax2.plot(sensor_890E_gyro_z, label='GYRO Z')
        ax2.set_title('Sensor 890E - Gyroscope')
        ax2.legend()

# Create an instance of FuncAnimation
ani = FuncAnimation(fig, animate, interval=100, cache_frame_data=False)

# Start the sensor manager
manager.start()

# Show the plot
plt.show()

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from CreaTeBME import SensorManager
from collections import deque
import numpy as np
import scipy.signal as signal

# Define the figure and axis using subplots
fig, ax = plt.subplots(figsize=(12, 6))

# Create a sensor manager for the given sensor names using the given callback
manager = SensorManager(['890E'])

# Sampling frequency of the sensor "890E"
fs = 101

# Create deque objects to store the sensor measurements with a maximum length of 500
sensor_890E_gyr_x = deque(maxlen=500)
sensor_890E_acc_x = deque(maxlen=500)
sensor_890E_acc_y = deque(maxlen=500)
sensor_890E_acc_z = deque(maxlen=500)
sensor_890E_acc_x_filtered = deque(maxlen=500)
sensor_890E_acc_y_filtered = deque(maxlen=500)
sensor_890E_acc_z_filtered = deque(maxlen=500)

# Initialize variables for angle estimation
gyr_x_angle = 0
complementary_weight = 0.01
angle_acc = np.empty(500)
angle_complementary = np.empty(500)

# Low-pass filter coefficients
fc = 1  # Cut-off frequency
w = (2 * fc / fs)
b, a = signal.butter(2, w, 'low')

# Animation update function
def animate(i):
    measurements = manager.get_measurements()

    for sensor, data in measurements.items():
        if not data:
            continue
        if len(data) > 0:  # Ensure data has at least 6 values
            if sensor == '890E':
                # Extract accelerometer and gyroscope values from each chunk
                for chunk in data:
                    acc_x, acc_y, acc_z, gyr_x, gyr_y, gyr_z = chunk
                    sensor_890E_acc_x.append(acc_x)  # Store accelerometer x
                    sensor_890E_acc_y.append(acc_y)  # Store accelerometer y
                    sensor_890E_acc_z.append(acc_z)  # Store accelerometer z
                    sensor_890E_gyr_x.append(gyr_x)  # Store gyroscope x

                # Apply low-pass filtering to accelerometer values
                sensor_890E_acc_x_filtered = signal.lfilter(b, a, sensor_890E_acc_x)
                sensor_890E_acc_y_filtered = signal.lfilter(b, a, sensor_890E_acc_y)
                sensor_890E_acc_z_filtered = signal.lfilter(b, a, sensor_890E_acc_z)

                # Calculate accelerometer angle estimation
                angle_acc_rads = np.arctan2(sensor_890E_acc_y_filtered, sensor_890E_acc_z_filtered)
                angle_acc_deg = np.degrees(angle_acc_rads)

                # Calculate complementary angle estimation
                rot_x_gyr = np.cumsum(sensor_890E_gyr_x) * (1 / fs)
                acc_x_array = np.array(sensor_890E_acc_x_filtered)
                acc_y_array = np.array(sensor_890E_acc_y_filtered)
                acc_z_array = np.array(sensor_890E_acc_z_filtered)
                rot_x_acc_rads = np.arctan(acc_y_array / np.sqrt(acc_x_array ** 2 + acc_z_array ** 2))
                rot_x_acc = np.degrees(rot_x_acc_rads)
                alpha = 0.01

                for i in range(len(sensor_890E_acc_x_filtered)):
                    if i == 0:
                        angle_complementary[i] = rot_x_acc[i]
                    else:
                        angle_complementary[i] = (1 - alpha) * (angle_complementary[i - 1] + sensor_890E_gyr_x[i] * (1 / fs)) + alpha * rot_x_acc[i]
                # for i in range(len(sensor_890E_acc_x_filtered)):
                #     angle_complementary[i] = (1 - alpha) * ( angle_complementary[i - 1] + sensor_890E_gyr_x[i] * (1 / fs)) + alpha * rot_x_acc[i]

    ax.clear()
    if sensor_890E_acc_x and sensor_890E_acc_y and sensor_890E_acc_z:
        ax.plot(angle_acc_deg, label='Accelerometer Angle')
        ax.plot(angle_complementary, label='Complementary Angle')
        ax.plot(rot_x_gyr, label='GYR Angle')
        ax.set_title('Sensor 890E - Angle Estimation')
        ax.legend()

# Create an instance of FuncAnimation
ani = FuncAnimation(fig, animate, interval=100, cache_frame_data=False)

# Start the sensor manager
manager.start()

# Show the plot
plt.show()

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from CreaTeBME import SensorManager
from collections import deque
import numpy as np
import scipy.signal as signal

# Define the figure and axis using subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6))

# Create a sensor manager for the given sensor names using the given callback
manager = SensorManager(['890E','7516'])

# Sampling frequency of the sensor "890E"
fs = 101

# Create deque objects to store the sensor measurements with a maximum length of 500
sensor_890E_gyr_x = deque(maxlen=500)
sensor_890E_gyr_y = deque(maxlen=500)
sensor_890E_gyr_z = deque(maxlen=500)
sensor_890E_acc_x = deque(maxlen=500)
sensor_890E_acc_y = deque(maxlen=500)
sensor_890E_acc_z = deque(maxlen=500)
sensor_890E_acc_x_filtered = deque(maxlen=500)
sensor_890E_acc_y_filtered = deque(maxlen=500)
sensor_890E_acc_z_filtered = deque(maxlen=500)
sensor_7516_gyr_x = deque(maxlen=500)
sensor_7516_gyr_y = deque(maxlen=500)
sensor_7516_gyr_z = deque(maxlen=500)
sensor_7516_acc_x = deque(maxlen=500)
sensor_7516_acc_y = deque(maxlen=500)
sensor_7516_acc_z = deque(maxlen=500)
sensor_7516_acc_x_filtered = deque(maxlen=500)
sensor_7516_acc_y_filtered = deque(maxlen=500)
sensor_7516_acc_z_filtered = deque(maxlen=500)

# Initialize variables for angle estimation
sensor_890E_gyr_x_angle = 0
sensor_890E_complementary_weight = 0.01
sensor_890E_angle_acc_deg = np.empty(500)
sensor_890E_angle_acc_rad = np.empty(500)
sensor_890E_angle_complementary = np.empty(500)
sensor_7516_gyr_x_angle = 0
sensor_7516_complementary_weight = 0.01
sensor_7516_angle_acc_deg = np.empty(500)
sensor_7516_angle_acc_rad = np.empty(500)
sensor_7516_angle_complementary = np.empty(500)
knee_angle_complementary = np.empty(500)
knee_angle = np.empty(500)

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
                    acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z = chunk
                    sensor_890E_acc_x.append(acc_x)
                    sensor_890E_acc_y.append(acc_y)
                    sensor_890E_acc_z.append(acc_z)
                    sensor_890E_gyr_x.append(gyro_x)
                    sensor_890E_gyr_y.append(gyro_y)
                    sensor_890E_gyr_z.append(gyro_z)

                # Apply low-pass filtering to accelerometer values
                sensor_890E_acc_x_filtered = signal.lfilter(b, a, sensor_890E_acc_x)
                sensor_890E_acc_y_filtered = signal.lfilter(b, a, sensor_890E_acc_y)
                sensor_890E_acc_z_filtered = signal.lfilter(b, a, sensor_890E_acc_z)

                # Calculate accelerometer angle estimation
                sensor_890_angle_acc_rads = np.arctan2(sensor_890E_acc_y_filtered, sensor_890E_acc_z_filtered)
                sensor_890_angle_acc_deg = np.degrees(sensor_890_angle_acc_rads)

                # Calculate complementary angle estimation
                sensor_890_rot_x_gyr = np.cumsum(sensor_890E_gyr_x) * (1 / fs)
                acc_x_array = np.array(sensor_890E_acc_x_filtered)
                acc_y_array = np.array(sensor_890E_acc_y_filtered)
                acc_z_array = np.array(sensor_890E_acc_z_filtered)
                rot_x_acc_rads = np.arctan(acc_y_array / np.sqrt(acc_x_array ** 2 + acc_z_array ** 2))
                rot_x_acc = np.degrees(rot_x_acc_rads)
                alpha = 0.01

                for i in range(len(sensor_890E_acc_x_filtered)):
                    sensor_890E_angle_complementary[i] = (1 - alpha) * ( sensor_890E_angle_complementary[i - 1] + sensor_890E_gyr_x[i] * (1 / fs)) + alpha * rot_x_acc[i]


            elif sensor == '7516':
                sensor_7516_angle_acc_deg = np.empty(500)
                # Extract accelerometer and gyroscope values from each chunk
                for chunk in data:
                    acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z = chunk
                    sensor_7516_acc_x .append(acc_x)
                    sensor_7516_acc_y .append(acc_y)
                    sensor_7516_acc_z .append(acc_z)
                    sensor_7516_gyr_x.append(gyro_x)
                    sensor_7516_gyr_y.append(gyro_y)
                    sensor_7516_gyr_z.append(gyro_z)

                # Apply low-pass filtering to accelerometer values
                sensor_7516_acc_x_filtered = signal.lfilter(b, a, sensor_7516_acc_x)
                sensor_7516_acc_y_filtered = signal.lfilter(b, a, sensor_7516_acc_y)
                sensor_7516_acc_z_filtered = signal.lfilter(b, a, sensor_7516_acc_z)

                # Calculate accelerometer angle estimation
                sensor_7516_angle_acc_rads = np.arctan2(sensor_7516_acc_y_filtered, sensor_7516_acc_z_filtered)
                sensor_7516_angle_acc_deg = np.degrees(sensor_7516_angle_acc_rads)

                # Calculate complementary angle estimation
                sensor_7516_rot_x_gyr = np.cumsum(sensor_7516_gyr_x) * (1 / fs)
                acc_x_array = np.array(sensor_7516_acc_x_filtered)
                acc_y_array = np.array(sensor_7516_acc_y_filtered)
                acc_z_array = np.array(sensor_7516_acc_z_filtered)
                rot_x_acc_rads = np.arctan(acc_y_array / np.sqrt(acc_x_array ** 2 + acc_z_array ** 2))
                rot_x_acc = np.degrees(rot_x_acc_rads)
                alpha = 0.01

                for i in range(len(sensor_7516_acc_x_filtered)):
                    if i == 0:
                        sensor_7516_angle_complementary[i] = rot_x_acc[i]
                    else:
                        sensor_7516_angle_complementary[i] = (1 - alpha) * ( sensor_7516_angle_complementary[i - 1] + sensor_7516_gyr_x[i] * (1 / fs)) + alpha * rot_x_acc[i]
                print(sensor_890E_angle_acc_deg)
                print(sensor_7516_angle_acc_deg)
                for i in range(len(sensor_7516_angle_acc_deg) ):
                    knee_angle_complementary[i] = sensor_890E_angle_acc_deg[i] - sensor_7516_angle_acc_deg[i]

    ax1.clear()
    if sensor_890E_acc_x and sensor_890E_acc_y and sensor_890E_acc_z:
        # ax1.plot(sensor_7516_rot_x_gyr, label='890E angle')
        # ax1.plot(sensor_7516_angle_acc_deg, label='7516 angle')
        # ax1.plot(sensor_890E_acc_z, label='ACC Z')
        ax1.set_title('Sensor 890E - Accelerometer')
        ax1.legend()

    ax2.clear()
    if sensor_7516_acc_x and sensor_7516_acc_y and sensor_7516_acc_z:
        ax2.plot(knee_angle_complementary, label='knee flexino angle')
        # ax2.plot(sensor_890E_gyro_y, label='GYRO Y')
        # ax2.plot(sensor_890E_gyro_z, label='GYRO Z')
        ax2.set_title('Sensor 890E - Gyroscope')
        ax2.legend()
# Create an instance of FuncAnimation
ani = FuncAnimation(fig, animate, interval=100, cache_frame_data=False)

# Start the sensor manager
manager.start()

# Show the plot
plt.show()
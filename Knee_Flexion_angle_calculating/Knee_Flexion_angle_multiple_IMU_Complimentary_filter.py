import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from CreaTeBME import SensorManager
from collections import deque
import scipy.signal as signal

# Define the figure and axis using subplots
fig, (ax1) = plt.subplots(1, 1, figsize=(12, 6))

# Create a sensor manager for the given sensor names using the given callback
manager = SensorManager(['890E', '7516'])

# Sampling frequency of the sensor "890E"
fs = 101

# Cut off frequency
fc = 1  # 1Hz

# Normalize the frequency relative to the Nyquist frequency
w = (2 * fc / fs)

# Create the numerator and denominator coefficients of the biquad filter
b, a = signal.butter(2, w, 'low')

# Create deque objects to store the sensor measurements with a maximum length of 500
# in order to find the angle around the z axis
sensor_890E_acc_x = deque(maxlen=500)
sensor_890E_acc_y = deque(maxlen=500)
sensor_7516_acc_x = deque(maxlen=500)
sensor_7516_acc_y = deque(maxlen=500)

sensor_890E_acc_x_filtered = deque(maxlen=500)
sensor_890E_acc_y_filtered = deque(maxlen=500)
sensor_7516_acc_x_filtered = deque(maxlen=500)
sensor_7516_acc_y_filtered = deque(maxlen=500)

sensor_890E_gyr_z = deque(maxlen=500)
sensor_7516_gyr_z = deque(maxlen=500)

sensor_890E_gyr_z_filtered = deque(maxlen=500)
sensor_7516_gyr_z_filtered = deque(maxlen=500)

sensor_890E_angle_acc_z = deque(maxlen=500)
sensor_890E_angle_gyr_z = deque(maxlen=500)
sensor_890E_angle_complimentary_z = deque(maxlen=500)
sensor_7516_angle_acc_z = deque(maxlen=500)
sensor_7516_angle_gyr_z = deque(maxlen=500)
sensor_7516_angle_complimentary_z = deque(maxlen=500)

knee_angle_complementary = deque(maxlen=500)

sensor_890E_angle_gyr_z.append(0)
sensor_890E_angle_complimentary_z.append(0)
sensor_7516_angle_gyr_z.append(0)
sensor_7516_angle_complimentary_z.append(0)

# Initialize previous input and output values for biquad filter
x1, x2, y1, y2 = 0, 0, 0, 0

# Biquad filter function
def biquad_filter(x0, b, a):
    global x1, x2, y1, y2  # Declare the variables as global
    y0 = x0 * b[0] + x1 * b[1] + x2 * b[2] - y1 * a[1] - y2 * a[2]
    x2, x1 = x1, x0
    y2, y1 = y1, y0
    return y0

# Animation update function
def animate(i):
    measurements = manager.get_measurements()
    gyr_ang = 0

    for sensor, data in measurements.items():
        if not data:
            continue
        if len(data) > 0:  # Ensure data has at least 6 values
            if sensor == '890E':
                # Extract accelerometer values from each chunk
                for chunk in data:
                    acc_x, acc_y, acc_z, gyr_x, gyr_y, gyr_z = chunk
                    sensor_890E_acc_x.append(acc_x)  # Store accelerometer x
                    sensor_890E_acc_y.append(acc_y)  # Store accelerometer y
                    sensor_890E_gyr_z.append(gyr_z)  # Store accelerometer y

                # Apply filtering to accelerometer values
                for x in sensor_890E_acc_x:
                    y = biquad_filter(x, b, a)
                    sensor_890E_acc_x_filtered.append(y)

                for x in sensor_890E_acc_y:
                    y = biquad_filter(x, b, a)
                    sensor_890E_acc_y_filtered.append(y)

                for x in sensor_890E_gyr_z:
                    y = biquad_filter(x, b, a)
                    sensor_890E_gyr_z_filtered.append(y)
                    # print(sensor_890E_gyr_z_filtered)

            for x in range(len(sensor_890E_acc_y_filtered)):
                 sensor_890E_angle_acc_z.append(np.arctan2(sensor_890E_acc_x_filtered[x], sensor_890E_acc_y_filtered[x])* (180 / np.pi))

            for x in range(len(sensor_890E_gyr_z_filtered)):
                gyr_ang+=sensor_890E_gyr_z_filtered[x] * (1 / fs)
                sensor_890E_angle_gyr_z.append(gyr_ang)


            for x in range(len(sensor_890E_gyr_z_filtered)):
                sensor_890E_angle_complimentary_z.append( 0.1 * sensor_890E_angle_acc_z[x] + 0.9 * sensor_890E_angle_gyr_z[x])

            if sensor == '7516':
                # Extract accelerometer values from each chunk
                for chunk in data:
                    acc_x, acc_y, acc_z, gyr_x, gyr_y, gyr_z = chunk
                    sensor_7516_acc_x.append(acc_x)  # Store accelerometer x
                    sensor_7516_acc_y.append(acc_y)  # Store accelerometer y
                    sensor_7516_gyr_z.append(gyr_z)  # Store accelerometer y

                # Apply filtering to accelerometer values
                for x in sensor_7516_acc_x:
                    y = biquad_filter(x, b, a)
                    sensor_7516_acc_x_filtered.append(y)

                for x in sensor_7516_acc_y:
                    y = biquad_filter(x, b, a)
                    sensor_7516_acc_y_filtered.append(y)

                for x in sensor_7516_gyr_z:
                    y = biquad_filter(x, b, a)
                    sensor_7516_gyr_z_filtered.append(y)
                    # print(sensor_7516_gyr_z_filtered)

            for x in range(len(sensor_7516_acc_y_filtered)):
                 sensor_7516_angle_acc_z.append(np.arctan2(sensor_7516_acc_x_filtered[x], sensor_7516_acc_y_filtered[x])* (180 / np.pi))

            for x in range(len(sensor_7516_gyr_z_filtered)):
                gyr_ang+=sensor_7516_gyr_z_filtered[x] * (1 / fs)
                sensor_7516_angle_gyr_z.append(gyr_ang)


            for x in range(len(sensor_7516_gyr_z_filtered)):
                sensor_7516_angle_complimentary_z.append( 0.1 * sensor_7516_angle_acc_z[x] + 0.9 * sensor_7516_angle_gyr_z[x])

            for x in range(len(sensor_7516_angle_complimentary_z)):
                knee_angle_complementary.append(sensor_890E_angle_complimentary_z[x] - sensor_7516_angle_complimentary_z[x])


    ax1.clear()
    if sensor_890E_angle_acc_z and sensor_890E_angle_gyr_z and sensor_890E_angle_complimentary_z :
        ax1.plot(knee_angle_complementary, label='comp angle flexion')
        ax1.set_title('Sensor 890E')
        ax1.legend()



# Create an instance of FuncAnimation
ani = FuncAnimation(fig, animate, interval=100, cache_frame_data=False)

# Start the sensor manager
manager.start()

# Show the plot
plt.show()

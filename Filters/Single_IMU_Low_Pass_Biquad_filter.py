import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from CreaTeBME import SensorManager
from collections import deque
import scipy.signal as signal

# Define the figure and axis using subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6))

# Create a sensor manager for the given sensor names using the given callback
manager = SensorManager(['890E'])

# Sampling frequency of the sensor "890E"
fs = 101

# Cut off frequency
fc = 1  # 1Hz

# Normalize the frequency relative to the Nyquist frequency
w = (2 * fc / fs)

# Create the numerator and denominator coefficients of the biquad filter
b, a = signal.butter(2, w, 'low')

# Create deque objects to store the sensor measurements with a maximum length of 500
sensor_890E_acc_x = deque(maxlen=500)
sensor_890E_acc_y = deque(maxlen=500)
sensor_890E_acc_z = deque(maxlen=500)

sensor_890E_acc_x_filtered = deque(maxlen=500)
sensor_890E_acc_y_filtered = deque(maxlen=500)
sensor_890E_acc_z_filtered = deque(maxlen=500)

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

    for sensor, data in measurements.items():
        if not data:
            continue
        if len(data) > 0:  # Ensure data has at least 6 values
            if sensor == '890E':
                # Extract accelerometer values from each chunk
                for chunk in data:
                    acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z = chunk
                    sensor_890E_acc_x.append(acc_x)  # Store accelerometer x
                    sensor_890E_acc_y.append(acc_y)  # Store accelerometer y
                    sensor_890E_acc_z.append(acc_z)  # Store accelerometer z

                # Apply filtering to accelerometer values
                for x in sensor_890E_acc_x:
                    y = biquad_filter(x, b, a)
                    sensor_890E_acc_x_filtered.append(y)

                for x in sensor_890E_acc_y:
                    y = biquad_filter(x, b, a)
                    sensor_890E_acc_y_filtered.append(y)

                for x in sensor_890E_acc_z:
                    y = biquad_filter(x, b, a)
                    sensor_890E_acc_z_filtered.append(y)

    ax1.clear()
    if sensor_890E_acc_x and sensor_890E_acc_y and sensor_890E_acc_z:
        ax1.plot(sensor_890E_acc_x, label='ACC X')
        ax1.plot(sensor_890E_acc_y, label='ACC Y')
        ax1.plot(sensor_890E_acc_z, label='ACC Z')
        ax1.set_title('Sensor 890E - Accelerometer')
        ax1.legend()

    ax2.clear()
    if sensor_890E_acc_x and sensor_890E_acc_y and sensor_890E_acc_z:
        ax2.plot(sensor_890E_acc_x_filtered, label='ACC X')
        ax2.plot(sensor_890E_acc_y_filtered, label='ACC Y')
        ax2.plot(sensor_890E_acc_z_filtered, label='ACC Z')
        ax2.set_title('Sensor 890E - Accelerometer - Filtered - Fc = 1Hz ')
        ax2.legend()

# Create an instance of FuncAnimation
ani = FuncAnimation(fig, animate, interval=100, cache_frame_data=False)

# Start the sensor manager
manager.start()

# Show the plot
plt.show()

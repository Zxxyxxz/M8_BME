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

#Cut off freqs
fc_1 = 15
fc_2 = 5
fc_3 = 1
fc_4 = 0.2

# Normalize the freuqency
# relative to the Nyquist frequency, which is half of the sampling frequency
w_1= (2*fc_1 / fs)
w_2= (2*fc_2 / fs)
w_3= (2*fc_3 / fs)
w_4= (2*fc_4 / fs)

b, a = signal.butter(2, w_1, 'low')
c, d = signal.butter(2, w_2, 'low')
e, f = signal.butter(2, w_3, 'low')
g, h = signal.butter(2, w_4, 'low')


# Create deque objects to store the sensor measurements and timestamps with a maximum length of 500
# deque supports setting a maximum length for the queue. When the queue reaches the maximum length, adding
# new elements to one end will automatically remove elements from the other end.

sensor_890E_acc_x = deque(maxlen=500)
sensor_890E_acc_y = deque(maxlen=500)
sensor_890E_acc_z = deque(maxlen=500)

sensor_890E_acc_x_filtered = deque(maxlen=500)
sensor_890E_acc_y_filtered = deque(maxlen=500)
sensor_890E_acc_z_filtered = deque(maxlen=500)


# Animation update function
def animate(i):
    measurements = manager.get_measurements()

    for sensor, data in measurements.items():
        if not data:
            continue
        if len(data) > 0:  # Ensure data has at least 6 values
            if sensor == '890E':
                # print(sensor, data)
                # print(data[0])

                # Extract accelerometer and gyroscope values from each chunk
                for chunk in data:
                    acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z = chunk
                    sensor_890E_acc_x.append(acc_x)  # Store accelerometer x
                    sensor_890E_acc_y.append(acc_y)  # Store accelerometer y
                    sensor_890E_acc_z.append(acc_z)  # Store accelerometer z

                # using 1Hz fc
                # Apply filtering to accelerometer values
                sensor_890E_acc_x_filtered = signal.lfilter(e, f, sensor_890E_acc_x)
                sensor_890E_acc_y_filtered= signal.lfilter(e, f, sensor_890E_acc_y)
                sensor_890E_acc_z_filtered = signal.lfilter(e, f, sensor_890E_acc_z)


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

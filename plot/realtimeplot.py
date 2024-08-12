import matplotlib.pyplot as plt
import matplotlib.animation as animation
import wfdb

# Load the WFDB record
record = wfdb.rdrecord('a03', pn_dir='apnea-ecg')
signal = record.p_signal[:, 0]

# Initialize the figure and axis
fig, ax = plt.subplots()
x_vals = []
y_vals = []

# Set the x-axis range based on the length of the signal
x_range = range(len(signal))

# Function to update the plot in real-time
def update(frame):
    x_vals.append(frame)
    y_vals.append(signal[frame])
    
    # Limit the number of points displayed to improve performance
    if len(x_vals) > 100:
        x_vals.pop(0)
        y_vals.pop(0)

    ax.clear()
    ax.plot(x_vals, y_vals)
    ax.set_title("Real-time ECG Signal")
    ax.set_xlabel("Sample Index")
    ax.set_ylabel("ECG Signal Value")

# Set up the animation
ani = animation.FuncAnimation(fig, update, frames=x_range, interval=10)

# Show the plot
plt.show()

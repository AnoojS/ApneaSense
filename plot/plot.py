import wfdb
import plotly.express as px

# Load the record
record = wfdb.rdrecord('a20', pn_dir='apnea-ecg')

# Extract the signal
signal = record.p_signal[:, 0]

# Specify start and end indices
start_index = 1 * record.fs
end_index = start_index + int(10 * record.fs)

# Create a Plotly Express line plot for the specified range
fig = px.line(y=signal[start_index:end_index], labels={'y': 'ECG Signal'}, title='ECG Signal Plot (Zoomed In)')

# Show the plot
fig.show()

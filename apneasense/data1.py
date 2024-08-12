import os
import django

from biosppy.signals import ecg
import matplotlib.pyplot as plt
import numpy as np
import wfdb
import random
import string
from scipy import signal

import tensorflow as tf

record = wfdb.rdrecord('x01', pn_dir='apnea-ecg')
p_signal = record.p_signal[:, 0]
fs = record.fs

# Load the model
model = tf.keras.models.load_model('sleep_apnea_detection_model.h5')

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])


#Filtering The Signal
low_cutoff = 3
high_cutoff = 45
b, a = signal.butter(4, [low_cutoff / (fs / 2), high_cutoff / (fs / 2)], btype='band')
filtered_signal = signal.filtfilt(b, a, p_signal)


#Detecting PQRST
rpeaks = ecg.ecg(signal=filtered_signal, sampling_rate=fs, show=False)
r_peaks_indices = rpeaks['rpeaks']

q_points_indices = []
s_points_indices = []
p_wave_indices = []
t_wave_indices = []

interval_duration = 0.08
interval_samples = int(interval_duration * fs)
for r_peak_index in r_peaks_indices:
    q_index = max(0, r_peak_index - interval_samples)
    s_index = min(len(filtered_signal) - 1, r_peak_index + interval_samples)
    q_point_index = np.argmin(filtered_signal[q_index:r_peak_index]) + q_index
    s_point_index = np.argmin(filtered_signal[r_peak_index:s_index]) + r_peak_index
    q_points_indices.append(q_point_index)
    s_points_indices.append(s_point_index)

p_wave_duration = 0.2
p_wave_samples = int(p_wave_duration * fs)
for q_index in q_points_indices:
    p_start_index = max(0, q_index - p_wave_samples)
    p_end_index = min(len(filtered_signal) - 1, q_index)
    p_wave_index = np.argmax(filtered_signal[p_start_index:q_index]) + p_start_index
    p_wave_indices.append(p_wave_index)

t_wave_duration = 0.4
t_wave_samples = int(t_wave_duration * fs)
for s_index in s_points_indices:
    t_start_index = max(0, s_index)
    t_end_index = min(len(filtered_signal) - 1, s_index + t_wave_samples)
    t_wave_index = np.argmax(filtered_signal[s_index:t_end_index]) + s_index
    t_wave_indices.append(t_wave_index)


#Dividing into windows
window_size = fs * 60
num_windows = len(filtered_signal) // window_size

window_arrays = []
for i in range(num_windows):
    start_index = i * window_size
    end_index = (i + 1) * window_size
    window_signal = filtered_signal[start_index:end_index]
    window_arrays.append(window_signal)
window_arrays = np.array(window_arrays)

window_r_peaks_indices = []
window_q_points_indices = []
window_s_points_indices = []
window_p_wave_indices = []
window_t_wave_indices = []
for i in range(num_windows):
    start_index = i * window_size
    end_index = (i + 1) * window_size

    window_r_peaks = [peak_idx - start_index for peak_idx in r_peaks_indices if start_index <= peak_idx < end_index]
    window_q_points = [q_idx - start_index for q_idx in q_points_indices if start_index <= q_idx < end_index]
    window_s_points = [s_idx - start_index for s_idx in s_points_indices if start_index <= s_idx < end_index]
    window_p_wave = [p_idx - start_index for p_idx in p_wave_indices if start_index <= p_idx < end_index]
    window_t_wave = [t_idx - start_index for t_idx in t_wave_indices if start_index <= t_idx < end_index]

    window_r_peaks_indices.append(window_r_peaks)
    window_q_points_indices.append(window_q_points)
    window_s_points_indices.append(window_s_points)
    window_p_wave_indices.append(window_p_wave)
    window_t_wave_indices.append(window_t_wave)


#Binary Representation of PQRST
binary_r_peaks = np.zeros_like(window_arrays)
binary_q_points = np.zeros_like(window_arrays)
binary_s_points = np.zeros_like(window_arrays)
binary_p_wave = np.zeros_like(window_arrays)
binary_t_wave = np.zeros_like(window_arrays)

for i in range(len(window_arrays)):
    binary_r_peaks[i, window_r_peaks_indices[i]] = 1
    binary_q_points[i, window_q_points_indices[i]] = 1
    binary_s_points[i, window_s_points_indices[i]] = 1
    binary_p_wave[i, window_p_wave_indices[i]] = 1
    binary_t_wave[i, window_t_wave_indices[i]] = 1


# Combine features and labels
features = np.concatenate((window_arrays[:, :, np.newaxis],
                            binary_r_peaks[:, :, np.newaxis],
                            binary_q_points[:, :, np.newaxis],
                            binary_s_points[:, :, np.newaxis],
                            binary_p_wave[:, :, np.newaxis],
                            binary_t_wave[:, :, np.newaxis],
                            ), axis=2)


test_X = features.tolist()

# Make predictions on the test data
predictions = model.predict(features)
predicted_labels = (predictions > 0.5).astype(int)

predicted_labels = predicted_labels.reshape(-1)
predicted_labels = predicted_labels.tolist()


duration = len(p_signal) / fs
time = np.linspace(0, duration, len(p_signal))

plt.xlabel('Time (seconds)')
plt.ylabel('Signal')
plt.title('ECG Signal')

plt.plot(time,p_signal,color='green')
folder_path = 'media/signals'
folder_path = os.path.join(os.getcwd(), folder_path)
length = 10
chars = string.ascii_letters + string.digits
random_string = ''.join(random.choice(chars) for _ in range(length))
file_name = random_string + ".jpg"

plt.savefig(os.path.join(folder_path, file_name), format='jpeg')


os.environ.setdefault('DJANGO_SETTINGS_MODULE','apneasense.settings')
django.setup()

from django.contrib.auth.models import User
from apneasense.models import Record

user = User.objects.get(username='anooj')
file_path = "signals/" + file_name

record=Record(
    x=test_X,
    user=user,
    prediction=predicted_labels,
    signal=file_path
)

record.save()
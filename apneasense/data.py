import os
import django


from scipy.signal import resample
import matplotlib.pyplot as plt
import numpy as np
import wfdb
import random
import string

records = ['a01', 'a02', 'a03', 'a04', 'a05', 'a06', 'a07', 'a08', 'a09', 'a10', 'a11', 'a12', 'a13', 'a14', 'a15', 'a16', 'a17', 'a18', 'a19', 'a20', 'b01', 'b02', 'b03', 'b04', 'b05', 'c01', 'c02', 'c03', 'c04', 'c05', 'c06', 'c07', 'c08', 'c09', 'c10']
i = random.randint(0, 34)
record = wfdb.rdrecord(records[i], pn_dir='apnea-ecg')
signal = record.p_signal[:, 0]

shape=signal.shape[0]
new_sample=100
shape=shape/new_sample
signal=resample(signal,int(shape))

test_X = signal.reshape(-1, 1)
test_X = test_X.tolist()

record = wfdb.rdrecord(records[i], pn_dir='apnea-ecg')
signal = record.p_signal[:, 0]
sampling_frequency = record.fs
duration = len(signal) / sampling_frequency
time = np.linspace(0, duration, len(signal))

plt.xlabel('Time (seconds)')
plt.ylabel('Signal')
plt.title('ECG Signal')

plt.plot(time,signal,color='green')
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
    signal=file_path
)

record.save()
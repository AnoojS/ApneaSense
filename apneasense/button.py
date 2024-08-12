import os
import django

from scipy.signal import resample
import matplotlib.pyplot as plt
import numpy as np
import wfdb

import tkinter as tk
from tkinter import messagebox
import threading
import time
import random
import string

class DataCollector:
    def __init__(self, root):
        self.root = root
        self.collecting = False

        self.collect_button = tk.Button(root, text="Collect", command=self.start_collecting)
        self.collect_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Stop", command=self.stop_collecting)
        self.stop_button.pack(pady=5)

        self.label = tk.Label(root, text="", font=("Arial", 12))
        self.label.pack(pady=10)

        self.data_label = tk.Label(root, text="", font=("Arial", 12))
        self.data_label.pack(pady=10)

        self.collected_data = []

        records = ['a01', 'a02', 'a03', 'a04', 'a05', 'a06', 'a07', 'a08', 'a09', 'a10', 'a11', 'a12', 'a13', 'a14', 'a15', 'a16', 'a17', 'a18', 'a19', 'a20', 'b01', 'b02', 'b03', 'b04', 'b05', 'c01', 'c02', 'c03', 'c04', 'c05', 'c06', 'c07', 'c08', 'c09', 'c10']
        i = random.randint(0, 34)
        self.record=wfdb.rdrecord(records[i], pn_dir='apnea-ecg')

    def start_collecting(self):
        if self.collecting:
            messagebox.showinfo("Info", "Data collection is already in progress.")
        else:
            self.collecting = True
            self.update_label("Data collecting")
            self.collect_button.configure(state=tk.DISABLED)
            self.stop_button.configure(state=tk.NORMAL)
            threading.Thread(target=self.collect_data).start()

    def stop_collecting(self):
        if self.collecting:
            self.collecting = False
            self.update_label("")
            self.collect_button.configure(state=tk.NORMAL)
            self.stop_button.configure(state=tk.DISABLED)
            self.process_data()
        else:
            messagebox.showinfo("Info", "No data collection is currently in progress.")

    def collect_data(self):
        i=0
        while self.collecting:
            signal = self.record.p_signal
            segment=signal[i]
            i+=1
            self.collected_data.append(segment)
            self.update_data_label(f"Collected data: {self.collected_data}")
            time.sleep(1/100)

    def update_label(self, text):
        self.label.configure(text=text)

    def update_data_label(self, text):
        self.data_label.configure(text=text)

    def process_data(self):
        self.collected_data=np.array(self.collected_data,dtype='float64')
        num_samples = len(self.collected_data)
        time_values = np.arange(0, num_samples) / 100
        signal=self.collected_data
        test_X = signal.reshape(-1, 1)
        test_X = test_X.tolist()

        plt.xlabel('Time (seconds)')
        plt.ylabel('Signal')
        plt.title('ECG Signal')
        plt.plot(time_values,self.collected_data,color='green')

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


        self.update_data_label("Data Collected Sucsessfully")
        self.collected_data = []

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Data Collection App")
    root.geometry("300x200")
    app = DataCollector(root)
    root.mainloop()

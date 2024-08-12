import threading
import subprocess

def run_script1():
    subprocess.call(["python", "button.py"])

def run_script2():
    subprocess.call(["python", "data_collection.py"])

thread1 = threading.Thread(target=run_script1)
thread2 = threading.Thread(target=run_script2)

thread1.start()
thread2.start()

thread1.join()
thread2.join()

print("Both scripts have finished running.")

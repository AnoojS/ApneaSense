import serial
import time

# Initialize serial communication with the specified baud rate
ser = serial.Serial('COM3', 9600)  # Change 'COM3' to the appropriate serial port on your system

# Initialize the pins
pin_22 = 22
pin_23 = 23
pin_4 = 4

# Main loop
while True:
    # Check if pin 22 or pin 23 is high
    if ser.read(pin_22) == 1 or ser.read(pin_23) == 1:
        # Send '!' over serial
        ser.write(b'!')
    else:
        # Send the value of analog input 0 over serial
        analog_value = ser.read(pin_4)
        ser.write(str(analog_value).encode())  # Convert integer to bytes and send
        print("Analog value from pin 4:", analog_value)  # Print analog value
        
    # Wait for a bit to prevent saturating serial data
    time.sleep(0.01)

import RPi.GPIO as GPIO
import time
import os
from aquarium_controller import servo_control,relay_control


# Setup GPIO mode
GPIO.setmode(GPIO.BOARD)

# Define relay pins corresponding to relays 0 to 3
relay_pins = [12, 10, 13, 11, 8, 7, 5, 3]

# Setup GPIO pins as output and initially set them to OFF
for pin in relay_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)  # Default to OFF

# Dictionary to keep track of the current state of each relay (True for ON, False for OFF)
relay_state = {i: False for i in range(len(relay_pins))}


# Function to read and process the relay file
def read_relay_file(file_path):
    relays_on = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                process_relay_command(line.strip(), relays_on)
    except FileNotFoundError:
        print("Relay and servo status file not found.")
        return

    # Turn OFF any relays not listed in the file but are currently ON
    for i, pin in enumerate(relay_pins):
        if i not in relays_on and relay_state[i]:  # If not in file and currently ON
            GPIO.output(pin, GPIO.HIGH)  # Turn relay OFF
            relay_state[i] = False      # Update the relay state
            print(f"Relay {i} (GPIO {pin}) is OFF (removed from file)")

# Process each line of the relay file (e.g., "Relay 0 on")
def process_relay_command(command, relays_on):
    parts = command.split()

    if len(parts) >= 3 and parts[0] == 'Relay':
        try:
            relay_index = int(parts[1])  # Get the relay number (0, 1, 2, 3)
            state = parts[2].lower()     # Get the state (on/off)

            if 0 <= relay_index < len(relay_pins):  # Validate relay index
                pin = relay_pins[relay_index]       # Get corresponding GPIO pin

                if state == 'on':
                    GPIO.output(pin, GPIO.LOW)   # Turn relay ON
                    relay_state[relay_index] = True  # Update relay state
                    relays_on.append(relay_index)    # Mark this relay as ON
                    print(f"Relay {relay_index} (GPIO {pin}) is ON")
                elif state == 'off':
                    GPIO.output(pin, GPIO.HIGH)    # Turn relay OFF
                    relay_state[relay_index] = False  # Update relay state
                    print(f"Relay {relay_index} (GPIO {pin}) is OFF")
        except ValueError:
            print("error relay Invalid command format")
            
    elif len(parts) >= 2 and parts[0] == 'Feeder' and parts[1] =='on':
        try:
            servo_control.turn_on_servo(90,0,'on',3)
            print(f"Servo is ON")
            relay_control.feeder_off()
            print(f"Servo is OFF")
            
            
        
            
        except ValueError:
            print(ValueError)    
    else:
        print("Invalid command format")

# Monitor for file changes
def monitor_relay_file(file_path, check_interval=1):
    last_modified_time = 5

    while True:
        # Get the last modified time of the file
        if os.path.exists(file_path):
            current_modified_time = os.path.getmtime(file_path)

            if current_modified_time != last_modified_time:
                print("File changed, reloading...")
                read_relay_file(file_path)  # Reload file if changed
                last_modified_time = current_modified_time
        else:
            print(f"File {file_path} does not exist.")

        # Wait before checking again
        time.sleep(check_interval)

# Example usage
relay_file_path = 'relay_status.txt'  # Path to your relay status text file

try:
    monitor_relay_file(relay_file_path)
finally:
    # Cleanup GPIO after use
    GPIO.cleanup()

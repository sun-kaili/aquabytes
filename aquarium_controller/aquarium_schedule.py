from aquarium_controller import relay_control
import time
from datetime import datetime


def load_schedule(filename):
    """Read the relay schedule from a text file and apply it."""
    with open(filename, 'r') as file:
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        for line in file:
            # Example line format: relay 0 time off 08:00 time on 20:00
            parts = line.split()

            if len(parts) >= 8:
                relay = int(parts[1])
                off_time = parts[4]  # Time to turn off the relay (e.g., 08:00)
                on_time = parts[7]   # Time to turn on the relay (e.g., 20:00)
                relay_state=relay_control.parse_relay_file()
                feeder_match=relay_control.parse_feeder()
                if parts[0] == 'relay':
                    if on_time == current_time:
                        a=f"relay{relay}"
                        #print(f"{a} on time scheduled parsing status")
                        if a not in relay_state:
                            relay_control.log_state(relay,"on")
                            print(f"Scheduled relay {relay}: ON at {on_time}")
            
                    if off_time == current_time:
                        a=f"relay{relay}"
                        #print(f"{a} off time scheduled parsing status")
                        if a in relay_state:
                            relay_control.remove_log_state(relay)
                            print(f"Scheduled relay {relay}: OFF at {off_time}")

                if parts[0] == 'feeder':
                    if on_time == current_time:
                        if feeder_match != True:
                            relay_control.feeder_on()
                            print(f"Scheduled Feeder: ON at {on_time}")
    
                    if off_time == current_time:
                        if feeder_match == True:
                            relay_control.feeder_off()
                            print(f"Scheduled Feeder: OFF at {off_time}")

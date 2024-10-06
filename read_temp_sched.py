import time
from aquarium_controller import sensor_temp,relay_control,aquarium_schedule

while True:
    try:
        aquarium_schedule.load_schedule("setting.txt")
        sensor_temp.get_all_data()
        temp=sensor_temp.get_temp_C_data()
        if temp > 32:
            relay_state=relay_control.parse_relay_file()
            if "relay2" not in relay_state:
                relay_control.log_state(2,"on")
            
            if "relay3" not in relay_state:
                relay_control.log_state(3,"on")
           
        
        

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        sensor_temp.dhtDevice.exit()
        raise error

    time.sleep(2.0)

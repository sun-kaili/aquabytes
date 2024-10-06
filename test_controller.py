import time
from aquarium_controller import aquarium_schedule

while True:
    try:
        aquarium_schedule.load_schedule("setting.txt")
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        raise error

    time.sleep(2.0)

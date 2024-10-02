import board
import adafruit_dht

dhtDevice = adafruit_dht.DHT11(board.D5)


# Function to get humidity and temperature
def get_all_data():

     # Print the values to the serial port
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity

        if humidity is not None and temperature_c is not None:
            return print(
                    "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                        temperature_f, temperature_c, humidity
                    )
                )
        else:
            return {'error': 'Sensor failure'}
        

def get_temp_C_data():
     
     if dhtDevice.temperature is not None:
        return dhtDevice.temperature

def get_temp_F_data():
     
     if dhtDevice.temperature is not None:
        return dhtDevice.temperature * (9 / 5) + 32
     
def get_humidity_data():
     
     if dhtDevice.humidity is not None:
        return dhtDevice.humidity

     
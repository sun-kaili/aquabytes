import re
import datetime
import sqlite3
import relay_control

# Database setup
def init_db():
    conn = sqlite3.connect('aquarium_automation.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS relay_schedule (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        relay_id INTEGER,
        on_time TEXT,
        off_time TEXT
    )
    ''')
    conn.commit()
    conn.close()

# Log relay state in the SQLite database
def log_setting(relay_id,on_time, off_time):
    conn = sqlite3.connect('aquarium_automation.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO relay_schedule (relay_id, on_time, off_time)
        VALUES (1, ?, ?)
    ''', (relay_id,on_time, off_time))
    conn.commit()
    conn.close()


def check_relay_schedule():
    conn = sqlite3.connect('aquarium_automation.db')
    cursor = conn.cursor()
    
    # Get the current time
    now = datetime.datetime.now().time()
    
    # Fetch all schedules
    cursor.execute('SELECT relay_id, on_time, off_time FROM relay_schedule')
    schedules = cursor.fetchall()

    for schedule in schedules:
        relay_id, on_time, off_time = schedule
        on_time = datetime.datetime.strptime(on_time, '%H:%M').time()
        off_time = datetime.datetime.strptime(off_time, '%H:%M').time()
        
        # Check if it's time to turn the relay on or off
        if on_time <= now <= off_time:
            # Turn the relay on
            print(f"Turning relay {relay_id} ON")
            relay_control.log_relay_state(relay_id, "on")
        else:
            # Turn the relay off
            print(f"Turning relay {relay_id} OFF")
            relay_control.log_relay_state(relay_id, "off")

    conn.close()

def remove_log_setting(relay_id):
    with open(relay_setting_file, "r") as fp:
        lines = fp.readlines()

    with open(relay_setting_file, "w") as fp:
        for line in lines:
            if line.strip("\n") != f"Relay {relay_id} on":
                fp.write(line)

def log_state(relay_id, state):
     # Open the log file and append the relay state and time
    with open(relay_setting_file, "a") as f:
        f.write(f"Relay {relay_id} {state}\n")
    return f"Relay {relay_id} logged as {state}"
import re
import datetime
import sqlite3

# Database setup
def init_db():
    conn = sqlite3.connect('aquarium_automation.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS relay_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        relay_id INTEGER,
        state TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    conn.close()

# Log relay state in the SQLite database
def log_relay_state(relay_id, state):
    conn = sqlite3.connect('aquarium_automation.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO relay_log (relay_id, state)
    VALUES (?, ?)
    ''', (relay_id, state))
    conn.commit()
    conn.close()

# Path to the text file storing relay states and timestamps
relay_state_file = 'relay_status.txt'

def parse_relay_file():
    relay_states = {}
    try:
        # Open and read the text file
        with open(relay_state_file, 'r') as file:
            lines = file.readlines()

        # Loop through each line and extract relay number, state, and timestamp
        for line in lines:
            # Use regular expression to extract the relay number, state, and timestamp
            match = re.match(r"Relay (\d+) (\w+)", line)
            if match:
                relay_number = int(match.group(1))  # Relay number (1, 2, 3, 4)
                state = match.group(2)  # "on" or "off"
                # Convert state to 1 for "on" and 0 for "off"
                  # Convert state to 1 for "on" and 0 for "off"
                relay_states[f'relay{relay_number}'] = 1 if state == "on" else 0
                    
    except FileNotFoundError:
        print(f"Error: {relay_state_file} not found.")
        # Default to all OFF if the file is not found
        for i in range(4):
            relay_states[f'relay_{i+1}'] = {
                "state": 0
                
            }

    return relay_states

def remove_log_state(relay_id):
    with open(relay_state_file, "r") as fp:
        lines = fp.readlines()

    with open(relay_state_file, "w") as fp:
        for line in lines:
            if line.strip("\n") != f"Relay {relay_id} on":
                fp.write(line)

def log_state(relay_id, state):
     # Open the log file and append the relay state and time
    with open(relay_state_file, "a") as f:
        f.write(f"Relay {relay_id} {state}\n")
    return f"Relay {relay_id} logged as {state}"
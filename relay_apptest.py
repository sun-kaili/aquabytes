from flask import Flask,jsonify
from flask_cors import CORS
from aquarium_controller import relay_control,sensor_temp

app = Flask(__name__)

@app.route('/logRelay/<int:relay_id>/<string:state>')
def logrelay(relay_id, state):
    relay_control.log_relay_state(relay_id, state)
    if state=="on":
        relay_control.log_state(relay_id, state)
    else:
         relay_control.remove_log_state(relay_id)

    return f"Relay {relay_id} logged as {state}"    

CORS(app, origins=["http://localhost","http://172.20.10.5","http://172.20.10.2","http://172.20.10.4"])
@app.route('/relay_status', methods=['GET'])
def get_relay_status():
    # Parse relay states from the file
    relay_states = relay_control.parse_relay_file()
    # Return the relay states as JSON
    return jsonify(relay_states)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

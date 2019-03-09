import smartcar
from flask import Flask, redirect, request, jsonify
from flask_cors import CORS

import os

app = Flask(__name__)
CORS(app)

# global variable to save our access_token
access = None

client = smartcar.AuthClient(
    client_id=os.environ.get('CLIENT_ID'),
    client_secret=os.environ.get('CLIENT_SECRET'),
    redirect_uri=os.environ.get('REDIRECT_URI'),
    scope=['read_vehicle_info read_odometer read_location control_security control_security:lock read_vin'],
    test_mode=True,
)

@app.route('/login', methods=['GET'])
def login():
    auth_url = client.get_auth_url()
    return redirect(auth_url)

@app.route('/exchange', methods=['GET'])
def exchange():
    # TODO: Authorization Step 3: Handle Smartcar response
    code = request.args.get('code')
    
    global access
    access = client.exchange_code(code)
    print(access['access_token'])

    return '', 200

@app.route('/vehicles', methods=['GET'])
def vehicle():
    vehicle_ids = smartcar.get_vehicle_ids(
        access['access_token'])['vehicles']

    response = []
    for i in range(len(vehicle_ids)):
        vehicle = smartcar.Vehicle(vehicle_ids[i], access['access_token'])

        info = vehicle.info()
        print(info)
        vin = vehicle.vin();
        print(vin)
        odometer = vehicle.odometer()
        print(odometer)
        location = vehicle.location()
        print(location)

        data = {"info":info, "vin":vin, "odometer":odometer, "location":location}
        response.append(data)

    return jsonify(response)

if __name__ == '__main__':
    app.run(port=8000)

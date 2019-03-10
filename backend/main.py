import smartcar
from flask import Flask, redirect, request, jsonify
from flask_cors import CORS

import os

app = Flask(__name__)
CORS(app)

# global variable to save our access_token
access = None

client = smartcar.AuthClient(
    client_id='e8236e6a-5e3d-4503-9b86-1e2181c6e4a8',
    client_secret='ffe4e263-fcd7-4223-a922-cfc65226eb8c',
    # redirect_uri='http://localhost:8000/exchange',
    redirect_uri= 'https://javascript-sdk.smartcar.com/redirect-2.0.0?app_origin=http://localhost:3000',
    scope=['read_vehicle_info read_odometer read_location control_security control_security:lock read_vin'],
    test_mode=True,
)

# @app.route('/login', methods=['GET'])
# def login():
#     auth_url = client.get_auth_url()
#     return redirect(auth_url)

@app.route('/exchange', methods=['GET'])
def exchange():
    # TODO: Authorization Step 3: Handle Smartcar response
    code = request.args.get('code')
    
    print("ID: " + str(code))

    global access
    access = client.exchange_code(code)

    return '', 200

@app.route('/vehicle', methods=['GET'])
def vehicle():
    vehicle_ids = smartcar.get_vehicle_ids(
        access['access_token'])['vehicles']

    response = []
    for i in range(len(vehicle_ids)):
        vehicle = smartcar.Vehicle(vehicle_ids[i], access['access_token'])

        info = vehicle.info()
        print(info)
        vin = vehicle.vin()
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

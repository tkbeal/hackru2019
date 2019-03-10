import smartcar
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flask import Flask, redirect, request, jsonify
from flask_cors import CORS

import json
import os

class Zone(object):
    def __init__(self, owner, hours_active_weekly = [], points = []):
        self.owner = owner
        self.hours_active_weekly = hours_active_weekly
        self.points = points

    @staticmethod
    def from_dict(source):
        return Zone(source['owner'], source['hours_active_weekly'], [(p.latitude, p.longitude) for p in source['points']])

    def to_dict_firebase(self):
        return {'owner' : self.owner, 'hours_active_weekly' : self.hours_active_weekly, 'points' : [GeoPoint(p.latitude, p.longitude) for p in self.points]}

    def to_dict(self):
        return {'owner' : self.owner, 'hours_active_weekly' : self.hours_active_weekly, 'points' : self.points}

    def __str__(self):
        return json.dumps(self.__dict__)

    def __repr__(self):
        return self.__str__()
    
app = Flask(__name__)
CORS(app)

#Firestore creds
cred = credentials.Certificate('../key.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

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
    user_id = request.args.get('user_id')
    user = db.collection(u'users').document(user_id).get().to_dict()

    code = request.args.get('code')
    
    global access
    access = client.exchange_code(code)
    print(access['access_token'])

    user['access_token'] = access['access_token']

    db.collection(u'users').document(user_id).set(user))

    return '', 200

@app.route('/zones', methods=['GET'])
def zones():
    user_id = request.args.get('user_id')
    docs = db.collection(u'zones').where(u'owner', u'==', user_id).get()

    resp = []

    for doc in docs:
        resp.append(Zone.from_dict(doc.to_dict()))

    print(resp)
    return "{" + str(resp) + "}"

@app.route('/zone', methods=['POST'])
def zone():
    pass

@app.route('/vehicles', methods=['GET'])
def vehicles:
    user_id = requests.args.get('user_id')
    
    user = db.collection.(u'users').document(user_id).get().to_dict()
    if user['access_token_expire_utc'] - time.time() < 60 * 5:
        True #Refresh token here
    
    access_token = user['access_token']

    vehicle_ids = smartcar.get_vehicle_ids(access_token)['vehicles']

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

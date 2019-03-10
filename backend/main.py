import smartcar

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from flask import Flask, redirect, request, jsonify
from flask_cors import CORS

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

import numpy as np
import json
import os
import threading

class Zone(object):
    def __init__(self, zone_id, owner, hours_active_weekly = [], points = []):
        self.owner = owner
        self.zone_id = zone_id
        self.hours_active_weekly = hours_active_weekly
        self.points = points

    @staticmethod
    def from_dict_firebase(source, zone_id):
        return Zone(source['owner'], zone_id, source['hours_active_weekly'], [(p.latitude, p.longitude) for p in source['points']])
    
    @staticmethod
    def from_dict_frontend(source, zone_id):
        return Zone(source['owner'], zone_id, source['hours_active_weekly'], source['points'])
    
    def to_dict_firebase(self):
        return {u'owner' : self.owner, u'hours_active_weekly' : self.hours_active_weekly, u'points' : [firestore.GeoPoint(p[0], p[1]) for p in self.points]}

    def to_dict(self):
        return {'owner' : self.owner, 'id' : zone_id, 'hours_active_weekly' : self.hours_active_weekly, 'points' : self.points}

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

    db.collection(u'users').document(user_id).set(user)

    return '', 200

@app.route('/zones', methods=['GET'])
def zones():
    user_id = request.args.get('user_id')
    docs = db.collection(u'zones').where(u'owner', u'==', user_id).get()

    resp = []

    for doc in docs:
        print(doc.id)
        resp.append(Zone.from_dict_firebase(doc.to_dict()))

    print(resp)
    return "{" + str(resp) + "}"

@app.route('/zone', methods=['POST'])
def zone():
    data = json.loads(request.data)
    zone = Zone.from_dict_frontend(data['zone'], data['id'])
    print(zone.zone_id)
    print(zone.to_dict)
    print(zone.to_dict_firebase)
    db.collection(u'zones').document(zone.zone_id).set(zone.to_dict_firebase())

    return '', 200

@app.route('/vehicles', methods=['GET'])
def vehicles():
    user_id = requests.args.get('user_id')
    
    user = db.collection(u'users').document(user_id).get().to_dict()
    if user['access_token_expire_utc'] - time.time() < 60 * 5:
        True #Refresh token here
    
    access_token = user['access_token']

    vehicle_ids = smartcar.get_vehicle_ids(access_token)['vehicles']

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

def vehiclesInZones():
    zones = db.collection(u'zones').get()

    for zone in zones:
        if isZoneActive(zone):
            poly = Polygon(zone.to_dict()["points"])

            user = db.collection(u'users').document(zone.to_dict()["owner"]).get().to_dict()
            if user['access_token_expire_utc'] - time.time() < 60 * 5:
                True #Refresh token here
        
            access_token = user['access_token']
            vehicles = smartcar.get_vehicle_ids(access_token)['vehicles']

            for i in range(len(vehicles)):
                vehicle = smartcar.Vehicle(vehicles[i], access_token)
                location = vehicle.location()
                point = Point(location.latitude, location.longitude)
                if not poly.contains(point):
                    True # Do something
    
    threading.Timer(60, vehiclesInZones).start()


def isZoneActive(zone):
    return True

if __name__ == '__main__':
    app.run(port=8000)

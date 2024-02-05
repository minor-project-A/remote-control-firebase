import firebase_admin
from firebase_admin import credentials,db


cred = credentials.Certificate('serviceAccount.json')
firebase_admin.initialize_app(cred,{'databaseURL':"https://remote-control-pi-6c1c2-default-rtdb.asia-southeast1.firebasedatabase.app"});

def get_data():
    try:
        root_ref = db.reference()
        containers_data = root_ref.child('containers').get()
        print(containers_data)
    except Exception as e:
        print(e)

get_data()

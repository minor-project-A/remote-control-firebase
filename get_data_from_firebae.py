
import firebase_admin
from firebase_admin import credentials, db
import datetime
import threading
import time

cred = credentials.Certificate('serviceAccount.json')
firebase_admin.initialize_app(cred, {'databaseURL': "https://remote-control-pi-6c1c2-default-rtdb.asia-southeast1.firebasedatabase.app"})

def set_alarm(alarm_time, medication_name):
    current_time = datetime.datetime.now().strftime('%H:%M')
    
    while current_time < alarm_time:
        time.sleep(1)
        current_time = datetime.datetime.now().strftime('%H:%M')
    
    print(f"Alarm set for {medication_name} at {alarm_time}! Time to take medication.")

def get_data_and_set_alarms():
    try:
        root_ref = db.reference()
        containers_data = root_ref.child('containers').get()
        
        for container_id, container_data in containers_data.items():
            medication_name = container_data.get('name', 'Unknown Medication')
            alarm_time = container_data.get('time', '')
            
            if alarm_time:
                print(f"Setting alarm for {medication_name} at {alarm_time}")
                threading.Thread(target=set_alarm, args=(alarm_time, medication_name)).start()
            else:
                print(f"No alarm set for {medication_name}")
                
    except Exception as e:
        print(e)

def periodic_update(interval_seconds):
    while True:
        get_data_and_set_alarms()
        time.sleep(interval_seconds)

# Set the interval for periodic updates (e.g., every 5 minutes)
update_interval_seconds = 60 

# Start the periodic update thread
threading.Thread(target=periodic_update, args=(update_interval_seconds,)).start()

# Keep the main thread alive
while True:
    time.sleep(1)


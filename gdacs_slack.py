import requests
import json
import os
from datetime import datetime, timedelta

SLACK_TRIGGER_URL = os.environ['SLACK_TRIGGER_URL']
API_URL = 'https://www.gdacs.org/gdacsapi/api/events/geteventlist/SEARCH'
STATE_FILE = 'last_eventid.txt'

def get_latest_eventid():
    try:
        with open(STATE_FILE, 'r') as f:
            return int(f.read().strip())
    except:
        return 0

def save_latest_eventid(eventid):
    with open(STATE_FILE, 'w') as f:
        f.write(str(eventid))

params = {
    'alertlevel': 'orange;red',
    'fromdate': (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
}
resp = requests.get(API_URL, params=params)
new_count = 0

if resp.status_code == 200:
    data = resp.json()
    events = data.get('Events', [])
    if events:
        latest_id = max(int(e['EventId']) for e in events)
        last_id = get_latest_eventid()
        new_events = [e for e in events if int(e['EventId']) > last_id]
        save_latest_eventid(latest_id)
        
        for event in new_events:
            payload = {
                'event_name': event['Name'],
                'country': event['Country'],
                'description': event['Description'][:200],
                'event_id': event['EventId'],
                'alert_level': event['AlertLevel']
            }
            requests.post(SLACK_TRIGGER_URL, json=payload)
            new_count += 1
        print(f"Triggered {new_count} new alerts")

print("GDACS check complete")

# Test

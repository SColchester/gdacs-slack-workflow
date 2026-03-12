import os
import requests

SLACK_TRIGGER_URL = os.environ['SLACK_TRIGGER_URL']

# Dummy orange alert for Spain test
payload = {
    'event_name': 'Test Orange GDACS alert',
    'country': 'PH',
    'description': 'Manual test: Orange alert simulation.',
    'event_id': 'TEST789',
    'alert_level': 'orange'
}

resp = requests.post(SLACK_TRIGGER_URL, json=payload)
if resp.status_code == 200:
    print("✅ Test alert posted to Slack Workflow!")
else:
    print(f"❌ Error: {resp.status_code} - {resp.text}")
# Index fix

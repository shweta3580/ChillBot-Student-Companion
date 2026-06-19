import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    try:
        creds = service_account.Credentials.from_service_account_file('service_account.json', scopes=SCOPES)
        return build('calendar', 'v3', credentials=creds)
    except Exception as e:
        print(f"Error loading service account credentials: {e}")
        return None

def list_events():
    try:
        service = get_calendar_service()
        events_result = service.events().list(
            calendarId='moresakshi385@gmail.com',
            maxResults=10,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])
        
        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(f"{start} - {event['summary']}")
    except Exception as e:
        print(f"Failed to list events: {e}")

def create_event():
    try:
        service = get_calendar_service()
        event = {
            'summary': 'Chill Bot Meeting',
            'location': 'Online',
            'description': 'Discussion on Chill Bot features.',
            'start': {'dateTime': (datetime.now() + timedelta(days=1)).isoformat(), 'timeZone': 'Asia/Kolkata'},
            'end': {'dateTime': (datetime.now() + timedelta(days=1, hours=1)).isoformat(), 'timeZone': 'Asia/Kolkata'},
            'reminders': {'useDefault': False, 'overrides': [{'method': 'email', 'minutes': 1440}, {'method': 'popup', 'minutes': 10}]}
        }
        event = service.events().insert(calendarId='moresakshi385@gmail.com', body=event).execute()
        print(f"Event created: {event.get('htmlLink')}")
    except Exception as e:
        print(f"Failed to create event: {e}")

def delete_event(event_id):
    try:
        service = get_calendar_service()
        service.events().delete(calendarId='moresakshi385@gmail.com', eventId=event_id).execute()
        print(f"Event {event_id} deleted.")
    except Exception as e:
        print(f"Failed to delete event: {e}")

if __name__ == '__main__':
    print("\nListing events:")
    list_events()
    
    print("\nCreating event:")
    create_event()
import os
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from ..obsidian_helper import load_config, write_to_file

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_calendar_events():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    now = datetime.utcnow().isoformat() + 'Z'
    end_time = (datetime.utcnow() + timedelta(days=1)).isoformat() + 'Z'

    events_result = service.events().list(calendarId='primary', timeMin=now, timeMax=end_time,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])
    return events

def generate_event_notes(events, config):
    vault_path = config['obsidian']['vault_path']
    notes_folder = os.path.join(vault_path, 'CalendarNotes')
    os.makedirs(notes_folder, exist_ok=True)

    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        summary = event['summary']
        description = event.get('description', '')
        location = event.get('location', '')

        note_content = f"# {summary}\n\n"
        note_content += f"**Start:** {start}\n"
        note_content += f"**Location:** {location}\n\n"
        note_content += f"**Description:**\n{description}\n"

        note_file = os.path.join(notes_folder, f"{summary}-{start}.md")
        write_to_file(note_file, note_content)

if __name__ == "__main__":
    config = load_config()
    events = get_calendar_events()
    generate_event_notes(events, config)
    print("Calendar event notes generated successfully.")

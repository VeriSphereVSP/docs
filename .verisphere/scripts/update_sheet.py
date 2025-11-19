import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

SPREADSHEET_NAME = "VeriSphere Bounty Ledger"

def extract_field(body, key):
    prefix = key + ":"
    for line in body.splitlines():
        if line.strip().startswith(prefix):
            return line.split(":", 1)[1].strip()
    return ""

def main():
    event_path = os.environ["GITHUB_EVENT_PATH"]
    with open(event_path, "r") as f:
        event = json.load(f)

    issue = event.get("issue", {})
    title = issue.get("title", "")
    url = issue.get("html_url", "")
    body = issue.get("body", "")

    # Extract fields
    task_id = extract_field(body, "Task ID")
    phase = extract_field(body, "Phase")
    hours = extract_field(body, "Estimated Hours")
    start_hour = extract_field(body, "Start Hour")
    end_hour = extract_field(body, "End Hour")
    bounty = extract_field(body, "Bounty (VSP)")
    dependencies = extract_field(body, "Dependencies")
    notes = extract_field(body, "Notes")

    # Sheets setup
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds_dict = json.loads(os.environ["GOOGLE_CREDENTIALS_JSON"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    gc = gspread.authorize(creds)
    sh = gc.open(SPREADSHEET_NAME)
    ws = sh.sheet1

    row = [
        task_id,
        phase,
        title,
        body,
        url,
        dependencies,
        hours,
        bounty,
        issue.get("state", ""),
        notes,
        "",  # TxID (Solscan) filled manually
        start_hour,
        end_hour,
    ]

    ws.append_row(row, value_input_option="RAW")
    print("Row appended to sheet:", row)

if __name__ == "__main__":
    main()


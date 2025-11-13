import os, json, re

def extract_label_value(labels, prefix):
    """
    Extracts values from labels like:
      phase:1
      bounty:50000
      hours:120
    """
    for l in labels:
        if l.lower().startswith(prefix.lower() + ":"):
            return l.split(":", 1)[1]
    return ""

def main():
    creds_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
    sheet_id = os.getenv("SHEET_ID")
    event_path = os.getenv("GITHUB_EVENT_PATH")

    print("🧾 Starting Sheets sync...")
    print("Event file:", event_path)

    if not os.path.exists(event_path):
        print("⚠️ No event file found.")
        return

    with open(event_path) as f:
        event = json.load(f)

    issue = event.get("issue", {})
    if not issue:
        print("⚠️ Not an issue event.")
        return

    number = issue.get("number", "")
    title = issue.get("title", "")
    body = issue.get("body", "")
    state = issue.get("state", "")
    labels = [l["name"] for l in issue.get("labels", [])]
    url = issue.get("html_url", "")

    print(f"Issue #{number}: {title}")
    print("Labels:", labels)

    # Parse structured label values
    phase = extract_label_value(labels, "phase")
    est_hours = extract_label_value(labels, "hours")
    bounty = extract_label_value(labels, "bounty")

    # Default status is GitHub state, but we prefer label if present
    status_label = extract_label_value(labels, "status")
    status = status_label if status_label else state

    # Unfilled fields can be added when governance approves the task
    dependencies = ""
    notes = ""
    txid = ""
    start_hour = ""
    end_hour = ""

    # Form the row with EXACT sheet schema
    row = [
        number,        # ID
        phase,         # Phase
        title,         # Task Name
        body,          # Full Description
        body,          # Deliverables (for now: duplicate body)
        dependencies,  # Dependencies
        est_hours,     # Est. Hours
        bounty,        # Bounty (VSP)
        status,        # Status
        notes,         # Notes
        txid,          # TxID
        start_hour,    # Start Hour N
        end_hour       # End Hour N
    ]

    print("Row to insert:", row)

    # Test mode
    if not creds_json:
        print("⚙️ No Google credentials provided — dry run.")
        return

    # Live Sheets update
    import gspread
    from google.oauth2.service_account import Credentials

    creds_dict = json.loads(creds_json)
    creds = Credentials.from_service_account_info(
        creds_dict,
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )

    client = gspread.authorize(creds)
    sheet = client.open_by_key(sheet_id).sheet1
    sheet.append_row(row)

    print("✅ Row appended to Google Sheet successfully!")


if __name__ == "__main__":
    main()


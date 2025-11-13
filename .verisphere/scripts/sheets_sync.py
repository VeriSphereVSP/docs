import os, json

def extract_label_value(labels, prefix):
    """Extract values from labels like:
       phase:1, hours:120, bounty:50000
    """
    prefix_lower = prefix.lower() + ":"
    for label in labels:
        if label.lower().startswith(prefix_lower):
            return label.split(":", 1)[1]
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

    # Extract GitHub issue fields
    number = issue.get("number", "")
    title = issue.get("title", "")
    body = issue.get("body", "")
    state = issue.get("state", "")
    url = issue.get("html_url", "")

    labels = [l["name"] for l in issue.get("labels", [])]

    print(f"Issue #{number}: {title}")
    print("Labels:", labels)

    # Label parsing
    phase = extract_label_value(labels, "phase")
    est_hours = extract_label_value(labels, "hours")
    bounty = extract_label_value(labels, "bounty")
    status_label = extract_label_value(labels, "status")
    status = status_label if status_label else state

    dependencies = ""
    deliverables = body  # you may later parse "### Deliverables" sections
    notes = ""
    txid = ""
    start_hour = ""
    end_hour = ""

    # New column ordering (includes URL)
    row = [
        number,        # ID (A)
        phase,         # Phase (B)
        title,         # Task Name (C)
        body,          # Full Description (D)
        url,           # URL (E) ← NEW
        deliverables,  # Deliverables (F)
        dependencies,  # Dependencies (G)
        est_hours,     # Est. Hours (H)
        bounty,        # Bounty (VSP) (I)
        status,        # Status (J)
        notes,         # Notes (K)
        txid,          # TxID (L)
        start_hour,    # Start Hour N (M)
        end_hour       # End Hour N (N)
    ]

    print("Row to insert:")
    print(row)

    # Exit early if no credentials — this prevents accidental writes
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


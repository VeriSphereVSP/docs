import os, json

def main():
    creds_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
    sheet_id = os.getenv("SHEET_ID")
    event_path = os.getenv("GITHUB_EVENT_PATH")

    print("🧾 Starting Sheets sync...")
    print(f"SHEET_ID: {sheet_id}")
    print(f"Event path: {event_path}")

    if not os.path.exists(event_path):
        print("⚠️ Event file not found. Exiting.")
        return

    with open(event_path) as f:
        event = json.load(f)

    issue = event.get("issue", {})
    number = issue.get("number")
    title = issue.get("title")
    state = issue.get("state")
    labels = [l["name"] for l in issue.get("labels", [])]
    url = issue.get("html_url")

    print(f"Issue #{number}: {title} [{state}]")
    print(f"Labels: {labels}")
    print(f"URL: {url}")

    # Test-only mode (no credentials)
    if not creds_json:
        print("⚙️ No Google credentials provided — dry run complete.")
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
    row = [number, title, state, ", ".join(labels), url]
    sheet.append_row(row)
    print("✅ Row appended to Google Sheet successfully!")

if __name__ == "__main__":
    main()


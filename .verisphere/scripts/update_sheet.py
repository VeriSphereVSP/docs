#!/usr/bin/env python3
import os
import json
import argparse
from datetime import datetime

import gspread
from google.oauth2.service_account import Credentials


def extract_field(body: str, key: str) -> str:
    """Extracts 'Key: value' fields from issue body text."""
    prefix = key + ":"
    for line in body.splitlines():
        if line.strip().startswith(prefix):
            return line.split(":", 1)[1].strip()
    return ""


def load_credentials():
    raw = os.environ.get("GOOGLE_CREDENTIALS_JSON")
    if not raw:
        raise SystemExit("ERROR: GOOGLE_CREDENTIALS_JSON missing.")

    try:
        creds_dict = json.loads(raw)
    except json.JSONDecodeError:
        raise SystemExit("ERROR: GOOGLE_CREDENTIALS_JSON invalid JSON.")

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    return Credentials.from_service_account_info(creds_dict, scopes=scopes)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sheet", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--body", required=True)
    parser.add_argument("--labels", required=True)
    parser.add_argument("--actor", required=True)
    parser.add_argument("--status", required=True)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--url", required=True)

    args = parser.parse_args()

    creds = load_credentials()
    gc = gspread.authorize(creds)

    try:
        sh = gc.open_by_key(args.sheet)
    except Exception as e:
        raise SystemExit(f"ERROR opening sheet by ID: {e}")

    ws = sh.sheet1

    body = args.body

    # Extract all structured fields
    task_id = extract_field(body, "Task ID")
    phase = extract_field(body, "Phase")
    hours = extract_field(body, "Estimated Hours")
    start_hour = extract_field(body, "Start Hour")
    end_hour = extract_field(body, "End Hour")
    bounty_vsp = extract_field(body, "Bounty (VSP)")
    dependencies = extract_field(body, "Dependencies")
    notes = extract_field(body, "Notes")

    # Parse labels JSON
    try:
        labels_json = json.loads(args.labels)
        labels_str = ", ".join(lbl["name"] for lbl in labels_json)
    except Exception:
        labels_str = args.labels

    timestamp = datetime.utcnow().isoformat()

    # Row layout matches your existing sheet
    row = [
        task_id,
        phase,
        args.title,
        body,
        args.url,
        dependencies,
        hours,
        bounty_vsp,
        args.status,
        notes,
        "",  # TxID (manual)
        start_hour,
        end_hour,
        labels_str,
        args.actor,
        args.repo,
        timestamp,
    ]

    ws.append_row(row, value_input_option="RAW")
    print("✔ Row appended:", row)


if __name__ == "__main__":
    main()


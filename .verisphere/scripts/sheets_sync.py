import os
import json
import re

def extract_label_value(labels, prefix):
    """
    Extract values from labels like:
       phase:1, hours:120, bounty:50000
    """
    prefix_lower = prefix.lower() + ":"
    for label in labels:
        if label.lower().startswith(prefix_lower):
            return label.split(":", 1)[1].strip()
    return ""


def extract_single_line_number(body, label):
    """
    Given a body and a label like 'Estimated Hours:',
    return a numeric string without commas, e.g. '600'.
    """
    pattern = rf"{re.escape(label)}\s*([0-9,\.]+)"
    m = re.search(pattern, body)
    if not m:
        return ""
    val = m.group(1).strip().replace(",", "")
    return val


def extract_block(body, start_label, end_label=None):
    """
    Extract a text block from body between `start_label` and `end_label`.
    If end_label is None, return from start_label to end-of-text.
    The returned string excludes the labels themselves.
    """
    start_pattern = re.escape(start_label)
    if end_label:
        end_pattern = re.escape(end_label)
        pattern = start_pattern + r"(.*?)(?:" + end_pattern + r"|$)"
    else:
        pattern = start_pattern + r"(.*)$"

    m = re.search(pattern, body, flags=re.S)
    if not m:
        return ""
    return m.group(1).strip()


def parse_issue_to_row(issue):
    """
    Convert a GitHub issue JSON object into a row matching:

    ID (A)
    Phase (B)
    Task Name (C)
    Full Description (D)
    Github Issue URL (E)
    Deliverables (F)
    Dependencies (G)
    Est. Hours (H)
    Bounty (VSP) (I)
    Status (J)
    Notes (K)
    TxID (Solscan) (L)
    Start Hour N (M)
    End Hour N (N)
    """
    number = issue.get("number", "")
    title  = issue.get("title", "") or ""
    body   = issue.get("body", "") or ""
    state  = issue.get("state", "") or ""
    url    = issue.get("html_url", "") or ""

    labels = [l["name"] for l in issue.get("labels", [])]

    # ---- Parse Task ID from body ----
    # Format: "Task ID: 2.1"
    m_id = re.search(r"Task ID:\s*([0-9.\-A-Za-z]+)", body)
    task_id = m_id.group(1).strip() if m_id else str(number)

    # ---- Phase ----
    # Either from body or from label "phase:x"
    m_phase = re.search(r"Phase:\s*([0-9]+)", body)
    phase_body = m_phase.group(1).strip() if m_phase else ""
    phase_label = extract_label_value(labels, "phase")
    phase = phase_body or phase_label

    # ---- Status ----
    status_label = extract_label_value(labels, "status")
    if status_label:
        status = status_label
    else:
        # map GH state to something useful
        status = "done" if state == "closed" else state

    # ---- Full Description ----
    full_description = body

    # ---- Deliverables block (between 'Deliverables:' and 'Dependencies:') ----
    deliverables = extract_block(body, "Deliverables:", "Dependencies:")

    # ---- Dependencies (between 'Dependencies:' and 'Estimated Hours:') ----
    dependencies = extract_block(body, "Dependencies:", "Estimated Hours:")

    # ---- Est. Hours ----
    est_hours = extract_single_line_number(body, "Estimated Hours:")
    # fallback to label if present
    if not est_hours:
        est_hours = extract_label_value(labels, "hours")

    # ---- Bounty (VSP) ----
    bounty = extract_single_line_number(body, "Bounty (VSP):")
    if not bounty:
        bounty = extract_label_value(labels, "bounty")

    # ---- Start / End Hour ----
    start_hour = extract_single_line_number(body, "Start Hour:")
    end_hour   = extract_single_line_number(body, "End Hour:")

    # ---- Notes ----
    # Everything after "Notes:" if present
    notes = extract_block(body, "Notes:") if "Notes:" in body else ""

    # ---- TxID (left blank unless you add logic later) ----
    txid = ""

    # Construct the row in column order A..N
    row = [
        task_id,        # A: ID
        phase,          # B: Phase
        title,          # C: Task Name
        full_description,  # D: Full Description
        url,            # E: Github Issue URL
        deliverables,   # F: Deliverables
        dependencies,   # G: Dependencies
        est_hours,      # H: Est. Hours
        bounty,         # I: Bounty (VSP)
        status,         # J: Status
        notes,          # K: Notes
        txid,           # L: TxID (Solscan)
        start_hour,     # M: Start Hour N
        end_hour        # N: End Hour N
    ]

    return task_id, row


def upsert_row(sheet, task_id, row):
    """
    Upsert into the sheet:
    - If a row with ID == task_id exists in column A, update that row.
    - Otherwise, append a new row.
    """
    # Get all IDs from column A
    id_col = sheet.col_values(1)  # 1-based index for column A
    target_row_index = None

    for idx, val in enumerate(id_col, start=1):
        if val.strip() == task_id:
            target_row_index = idx
            break

    if target_row_index is None:
        # Append new row
        sheet.append_row(row, value_input_option="RAW")
        print(f"✅ Appended new row for Task ID {task_id}")
    else:
        # Update existing row A..N
        cell_range = f"A{target_row_index}:N{target_row_index}"
        sheet.update(cell_range, [row], value_input_option="RAW")
        print(f"✅ Updated existing row {target_row_index} for Task ID {task_id}")


def main():
    creds_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
    sheet_id   = os.getenv("SHEET_ID")
    event_path = os.getenv("GITHUB_EVENT_PATH")

    print("🧾 Starting Sheets sync (UPSERT)...")
    print("Event file:", event_path)

    if not event_path or not os.path.exists(event_path):
        print("⚠️ No event file found.")
        return

    with open(event_path) as f:
        event = json.load(f)

    issue = event.get("issue", {})
    if not issue:
        print("⚠️ Not an issue event.")
        return

    # Get labels and ensure there's a bounty label (safety, redundant with workflow guard)
    labels = [lbl["name"] for lbl in issue.get("labels", [])]
    if not any(l == "bounty" or l.startswith("bounty:") for l in labels):
        print("⚠️ No bounty label present; skipping Sheets sync.")
        return

    # Parse issue → row
    task_id, row = parse_issue_to_row(issue)

    print(f"Issue #{issue.get('number')} → Task ID {task_id}")
    print("Row to upsert:")
    print(row)

    # Exit early if no credentials — prevents accidental writes
    if not creds_json:
        print("⚙️ No GOOGLE_CREDENTIALS_JSON provided — dry run only.")
        return

    if not sheet_id:
        print("⚙️ No SHEET_ID provided — cannot update sheet.")
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

    # If your ledger is not the first sheet, you can replace `sheet1`
    # with e.g. client.open_by_key(sheet_id).worksheet("VeriSphere Bounty Ledger")
    sheet = client.open_by_key(sheet_id).sheet1

    upsert_row(sheet, task_id, row)

    print("✅ Sheets sync complete.")


if __name__ == "__main__":
    main()


#!/usr/bin/env python3
"""
create_issues_from_csv.py

Creates GitHub issues from a CSV file and forces a labeled event so that
bounty.yaml appends the issue row to the Google Sheet.

Place this file in: verisphere/docs/create_issues_from_csv.py
Run with:
    GITHUB_TOKEN=ghp_xxx python3 create_issues_from_csv.py mytasks.csv
"""

import os
import csv
import sys
import time
import requests

# ----------------------------------------------------------
# CONFIG
# ----------------------------------------------------------
REPO = "VeriSphereVSP/docs"
TOKEN = os.environ.get("GITHUB_TOKEN")

if not TOKEN:
    raise SystemExit("ERROR: GITHUB_TOKEN environment variable is not set.")

ISSUES_API = f"https://api.github.com/repos/{REPO}/issues"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
}


# ----------------------------------------------------------
# UTIL — Check if the issue already exists
# ----------------------------------------------------------
def github_issue_exists(title: str) -> bool:
    """Return True if an issue with this title already exists."""
    resp = requests.get(ISSUES_API, headers=HEADERS, params={"state": "all", "per_page": 100})
    if resp.status_code != 200:
        print("⚠️ Could not fetch existing issues:", resp.text[:200])
        return False

    for issue in resp.json():
        if issue.get("title", "").strip() == title.strip():
            print(f"⚠️ Issue already exists → {issue['html_url']}")
            return True
    return False


# ----------------------------------------------------------
# UTIL — Force labeled webhook to fire so bounty.yaml runs
# ----------------------------------------------------------
def force_labeled_event(issue_number: int, labels: list[str]):
    """
    To ensure our Google Sheet workflow runs, we PATCH the issue
    with its existing labels, forcing GitHub to emit a "labeled" event.
    """
    url = f"{ISSUES_API}/{issue_number}"
    resp = requests.patch(url, headers=HEADERS, json={"labels": labels})

    if resp.status_code >= 300:
        print("❌ Failed to trigger labeled event:", resp.status_code, resp.text[:300])
    else:
        print("🔄 Labeled event triggered successfully.")


# ----------------------------------------------------------
# MAIN
# ----------------------------------------------------------
def main():
    # CSV argument
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "verisphere_mvp_tasks.csv"
    print("📄 Using CSV:", csv_path)

    # Load CSV
    try:
        f = open(csv_path, newline="", encoding="utf-8")
    except FileNotFoundError:
        raise SystemExit(f"ERROR: CSV file not found: {csv_path}")

    with f:
        reader = csv.DictReader(f)

        for row in reader:
            title = (row.get("Title") or "").strip()
            body = (row.get("Body") or "").strip()
            labels_raw = (row.get("Labels") or "").split(",")

            if not title:
                print("⚠️ Skipping row with empty title")
                continue

            # Normalize labels
            labels = [l.strip() for l in labels_raw if l.strip()]
            if "bounty" not in [l.lower() for l in labels]:
                labels.append("bounty")

            print(f"\n🛠 Preparing issue: {title}")

            # Skip duplicates
            if github_issue_exists(title):
                continue

            # Create issue
            payload = {"title": title, "body": body, "labels": labels}
            resp = requests.post(ISSUES_API, headers=HEADERS, json=payload)

            if resp.status_code >= 300:
                print("❌ Error creating issue:", resp.status_code, resp.text[:300])
                continue

            issue = resp.json()
            issue_number = issue["number"]
            issue_url = issue["html_url"]

            print(f"✅ Created issue: {issue_url}")

            # Force GitHub to emit a labeled event so bounty.yaml runs
            time.sleep(1)
            force_labeled_event(issue_number, labels)


if __name__ == "__main__":
    main()


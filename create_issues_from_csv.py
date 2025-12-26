#!/usr/bin/env python3
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
from transformers import BertTokenizer, BertModel

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

# Embedding service
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

def get_embedding(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
    return embeddings

def cosine_similarity(embedding1, embedding2):
    dot_product = np.dot(embedding1, embedding2)
    norm1 = np.linalg.norm(embedding1)
    norm2 = np.linalg.norm(embedding2)
    similarity = dot_product / (norm1 * norm2)
    return similarity

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

        embeddings = {}
        for row in reader:
            title = (row.get("Title") or "").strip()
            body = (row.get("Body") or "").strip()

            if not title:
                print("⚠️ Skipping row with no Title")
                continue

            # Check if the issue already exists
            if github_issue_exists(title):
                print(f"Skipping duplicate issue: {title}")
                continue

            # Generate embeddings for existing issues (assuming they are in a separate CSV)
            if not embeddings:
                with open("existing_issues.csv", newline="", encoding="utf-8") as ef:
                    e_reader = csv.DictReader(ef)
                    for e_row in e_reader:
                        e_title = (e_row.get("Title") or "").strip()
                        e_body = (e_row.get("Body") or "").strip()
                        if e_title and e_body:
                            embeddings[e_title] = get_embedding(e_body)

            # Check similarity with existing issues
            max_similarity = 0.8
            for e_title, e_embedding in embeddings.items():
                new_embedding = get_embedding(body)
                similarity = cosine_similarity(new_embedding, e_embedding)
                if similarity > max_similarity:
                    print(f"Skipping potential duplicate issue: {title} (similarity: {similarity})")
                    continue

            # Force labeled event to update Google Sheet
            force_labeled_event(1, labels_raw)  # Assuming issue number is 1 for demonstration


if __name__ == "__main__":
    main()
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


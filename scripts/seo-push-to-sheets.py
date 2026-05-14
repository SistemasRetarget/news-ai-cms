#!/usr/bin/env python3
"""
Push SEO + CTA report results to Google Sheets.

Creates or appends to a 'SEO Reports' tab in the Retarget Gantt sheet.

Usage:
  python3 scripts/seo-push-to-sheets.py --seo /tmp/seo-reports/seo-XYZ.json --cta /tmp/seo-reports/cta-XYZ.json
  python3 scripts/seo-push-to-sheets.py --seo /tmp/seo-reports/seo-XYZ.json --cta /tmp/seo-reports/cta-XYZ.json --lh-perf 85 --lh-seo 92
"""

import sys
import json
import argparse
import os
from datetime import datetime

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

from google.oauth2 import service_account
from googleapiclient.discovery import build

CREDENTIALS_FILE = os.environ.get(
    "GCP_CREDENTIALS_FILE",
    "/Users/spam11/Desktop/RETARGET-WORKSPACE/retarget-mcp-2d37bb49c600.json"
)
SHEET_ID = "1murmG-pdc5GkJ1CYc4_1UISRTcipMxPYv2jiH_-7ZIY"
TAB_NAME = "SEO Reports"

HEADERS = [
    "Fecha", "URL", "SEO Score", "CTA Score",
    "LH Performance", "LH SEO", "LH Accessibility", "LH Best Practices",
    "CTAs detectados", "GA4 Coverage %",
    "Issues SEO", "Issues CTA", "CTA Strategy"
]


def get_service():
    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE,
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    return build("sheets", "v4", credentials=creds, cache_discovery=False)


def ensure_tab(service):
    """Create 'SEO Reports' tab if it doesn't exist."""
    sheet_meta = service.spreadsheets().get(spreadsheetId=SHEET_ID).execute()
    existing = [s["properties"]["title"] for s in sheet_meta["sheets"]]

    if TAB_NAME not in existing:
        body = {"requests": [{"addSheet": {"properties": {"title": TAB_NAME}}}]}
        service.spreadsheets().batchUpdate(spreadsheetId=SHEET_ID, body=body).execute()
        # Write headers
        service.spreadsheets().values().update(
            spreadsheetId=SHEET_ID,
            range=f"'{TAB_NAME}'!A1",
            valueInputOption="USER_ENTERED",
            body={"values": [HEADERS]}
        ).execute()
        # Bold headers
        sheet_meta2 = service.spreadsheets().get(spreadsheetId=SHEET_ID).execute()
        sheet_id = next(
            s["properties"]["sheetId"]
            for s in sheet_meta2["sheets"]
            if s["properties"]["title"] == TAB_NAME
        )
        service.spreadsheets().batchUpdate(
            spreadsheetId=SHEET_ID,
            body={"requests": [{
                "repeatCell": {
                    "range": {"sheetId": sheet_id, "startRowIndex": 0, "endRowIndex": 1},
                    "cell": {"userEnteredFormat": {"textFormat": {"bold": True}}},
                    "fields": "userEnteredFormat.textFormat.bold"
                }
            }]}
        ).execute()
        print(f"✅ Tab '{TAB_NAME}' created with headers")
    else:
        print(f"✅ Tab '{TAB_NAME}' exists")


def build_row(seo_data, cta_data, lh_perf, lh_seo, lh_acc, lh_bp):
    url = seo_data.get("url", cta_data.get("url", ""))
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")

    seo_score = seo_data.get("score", "")
    cta_score = cta_data.get("score", "")

    cta_count = cta_data.get("cta_count", 0)
    ga4_coverage = cta_data.get("tracking", {}).get("coverage", 0)

    seo_issues = " | ".join([
        i for i in seo_data.get("issues", [])
        if i and i.startswith("❌")
    ][:3]) or "OK"

    cta_suggestions = " | ".join(cta_data.get("suggestions", [])[:2]) or "OK"
    cta_strategy = " | ".join(cta_data.get("strategy", [])[:2]) or ""

    return [
        fecha, url,
        seo_score, cta_score,
        lh_perf or "N/A", lh_seo or "N/A", lh_acc or "N/A", lh_bp or "N/A",
        cta_count, ga4_coverage,
        seo_issues, cta_suggestions, cta_strategy
    ]


def push_report(seo_file, cta_file, lh_perf=None, lh_seo=None, lh_acc=None, lh_bp=None):
    with open(seo_file) as f:
        seo_data = json.load(f)
    with open(cta_file) as f:
        cta_data = json.load(f)

    service = get_service()
    ensure_tab(service)

    row = build_row(seo_data, cta_data, lh_perf, lh_seo, lh_acc, lh_bp)

    service.spreadsheets().values().append(
        spreadsheetId=SHEET_ID,
        range=f"'{TAB_NAME}'!A1",
        valueInputOption="USER_ENTERED",
        insertDataOption="INSERT_ROWS",
        body={"values": [row]}
    ).execute()

    url = seo_data.get("url", "")
    print(f"✅ Report pushed to Sheets: SEO={row[2]} CTA={row[3]} GA4={row[9]}% — {url}")
    print(f"   https://docs.google.com/spreadsheets/d/{SHEET_ID}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--seo", required=True, help="Path to seo-validator JSON output")
    parser.add_argument("--cta", required=True, help="Path to cta-analyzer JSON output")
    parser.add_argument("--lh-perf", help="Lighthouse performance score")
    parser.add_argument("--lh-seo", help="Lighthouse SEO score")
    parser.add_argument("--lh-acc", help="Lighthouse accessibility score")
    parser.add_argument("--lh-bp", help="Lighthouse best practices score")
    args = parser.parse_args()

    push_report(args.seo, args.cta, args.lh_perf, args.lh_seo, args.lh_acc, args.lh_bp)

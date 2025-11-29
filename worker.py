import time
import requests
import uuid
from settings import BACKEND_URL, LOCK_CODE
from pdf_utils import generate_summary_pdf, generate_invoice_pdf, encrypt_pdf
from email_utils import send_report_email

import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MESHY_API_KEY = os.getenv("MESHY_API_KEY")
PRINTIFY_API_KEY = os.getenv("PRINTIFY_API_KEY")
GUMROAD_TOKEN = os.getenv("GUMROAD_ACCESS_TOKEN")
PAYHIP_API_KEY = os.getenv("PAYHIP_API_KEY")


def fetch_task():
    try:
        r = requests.get(f"{BACKEND_URL}/task/next")
        return r.json()
    except:
        return {"status": "error"}


def mark_done(task_id):
    requests.post(f"{BACKEND_URL}/task/done/{task_id}")


def process_daily_report(task):
    print("🟦 Generating Daily Report...")

    # Fake example data (replace later with real data)
    summary_data = [
        "JRAVIS completed your tasks.",
        "Income streams processed.",
        "No issues detected."
    ]
    invoice_data = [
        "Invoice #001 – ₹5000",
        "Invoice #002 – ₹12000",
    ]

    # Paths
    summary = "summary.pdf"
    locked_summary = "summary_locked.pdf"
    invoice = "invoice.pdf"

    generate_summary_pdf(summary, summary_data)
    encrypt_pdf(summary, locked_summary, LOCK_CODE)
    generate_invoice_pdf(invoice, invoice_data)

    approval_token = str(uuid.uuid4())

    send_report_email(locked_summary, invoice, approval_token)

    print("✔ Daily report emailed.")

    # Schedule worker to wait and auto-resume
    time.sleep(600)
    print("⏳ 10 minutes passed — auto-resume JRAVIS.")


def process_weekly_report(task):
    print("🟪 Generating Weekly Report...")

    # Replace with real logic later
    summary_data = ["Weekly stats summary"]
    invoice_data = ["Weekly invoice"]

    summary = "week_summary.pdf"
    locked_summary = "week_summary_locked.pdf"
    invoice = "week_invoice.pdf"

    generate_summary_pdf(summary, summary_data)
    encrypt_pdf(summary, locked_summary, LOCK_CODE)
    generate_invoice_pdf(invoice, invoice_data)

    approval_token = str(uuid.uuid4())
    send_report_email(locked_summary, invoice, approval_token)

    time.sleep(600)
    print("Weekly auto-resume complete.")


def run_worker():
    print("🚀 JRAVIS Worker started…")

    while True:
        task = fetch_task()

        if task.get("status") == "empty":
            time.sleep(2)
            continue

        if "task" not in task:
            time.sleep(1)
            continue

        t = task["task"]

        if t["type"] == "daily_report":
            process_daily_report(task)
        elif t["type"] == "weekly_report":
            process_weekly_report(task)
        elif t["type"] == "approval_received":
            print("Boss approved — JRAVIS resuming…")

        mark_done(task["id"])
        time.sleep(1)


if __name__ == "__main__":
    run_worker()

import os
from datetime import date

LOCK_FILE = "data/last_run.txt"

def already_ran_today():
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists(LOCK_FILE):
        return False
    with open(LOCK_FILE, "r") as f:
        return f.read().strip() == str(date.today())

def mark_ran_today():
    with open(LOCK_FILE, "w") as f:
        f.write(str(date.today()))

def run_all():
    if already_ran_today():
        print("⏹ Already ran today. Skipping.")
        return

    from workers.gumroad_prep_worker import run_gumroad_prep
    from workers.payhip_prep_worker import run_payhip_prep
    from workers.webflow_draft_worker import run_webflow
    from workers.blogger_draft_worker import run_blogger
    from workers.affiliate_draft_worker import run_affiliate
    from workers.newsletter_draft_worker import run_newsletter

    run_gumroad_prep()
    run_payhip_prep()
    run_webflow()
    run_blogger()
    run_affiliate()
    run_newsletter()

    mark_ran_today()
    print("✅ Draft cycle completed for today")

if __name__ == "__main__":
    run_all()
    

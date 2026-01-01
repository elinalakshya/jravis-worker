from workers.gumroad_prep_worker import run_gumroad_prep
from workers.payhip_prep_worker import run_payhip_prep
from workers.webflow_draft_worker import run_webflow
from workers.blogger_draft_worker import run_blogger
from workers.affiliate_draft_worker import run_affiliate
from workers.newsletter_draft_worker import run_newsletter

def run_all():
    run_gumroad_prep()
    run_payhip_prep()
    run_webflow()
    run_blogger()
    run_affiliate()
    run_newsletter()

if __name__ == "__main__":
    run_all()

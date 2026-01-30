import requests
import os
from datetime import datetime, timedelta

# =========================
# SETTINGS
# =========================

START_DATE = "2023-01-01"
END_DATE   = "2025-12-31"

OLD_BOX_SUMMARY = "https://raw.githubusercontent.com/unknownman2024/assetz/refs/heads/main/daily/olddata/{date}_summary.json"

NEW_BOX_SUMMARY = "https://raw.githubusercontent.com/unknownman2024/assetz/refs/heads/main/advance/data/{compact}/finalsummary.json"
NEW_BOX_DETAILED = "https://raw.githubusercontent.com/unknownman2024/assetz/refs/heads/main/advance/data/{compact}/finaldetailed.json"

OLD_ADVANCE = "https://bfilmy.pages.dev/Daily%20Advance/data/{date}.json"


# =========================
# HELPERS
# =========================

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def download(url, path):
    try:
        r = requests.get(url, timeout=30)

        if r.status_code == 200:
            with open(path, "wb") as f:
                f.write(r.content)

            print("✔ Saved:", path)
            return True

        return False

    except Exception as e:
        print("❌ Error:", url, e)
        return False


def daterange(start, end):
    s = datetime.strptime(start, "%Y-%m-%d")
    e = datetime.strptime(end, "%Y-%m-%d")

    while s <= e:
        yield s
        s += timedelta(days=1)


# =========================
# MAIN
# =========================

def main():

    for d in daterange(START_DATE, END_DATE):

        date_str = d.strftime("%Y-%m-%d")
        compact  = d.strftime("%Y%m%d")
        year     = d.strftime("%Y")
        md       = d.strftime("%m-%d")

        print("\n📅 Processing:", date_str)

        # ===============================
        # BOXOFFICE
        # ===============================

        daily_dir = f"daily/data/{year}"
        ensure_dir(daily_dir)

        summary_path = f"{daily_dir}/{md}_finalsummary.json"
        detailed_path = f"{daily_dir}/{md}_finaldetailed.json"

        # Old format (before 2025-12-20)
        if d < datetime(2025, 12, 20):

            old_summary_url = OLD_BOX_SUMMARY.format(date=date_str)

            ok = download(old_summary_url, summary_path)

            if not ok:
                print("⚠ Missing:", old_summary_url)

        # New format (from 2025-12-20)
        else:

            new_sum = NEW_BOX_SUMMARY.format(compact=compact)
            new_det = NEW_BOX_DETAILED.format(compact=compact)

            download(new_sum, summary_path)
            download(new_det, detailed_path)


        # ===============================
        # ADVANCE
        # ===============================

        adv_dir = f"advance/data/{year}"
        ensure_dir(adv_dir)

        adv_sum_path = f"{adv_dir}/{md}_finalsummary.json"
        adv_det_path = f"{adv_dir}/{md}_finaldetailed.json"

        # Old advance
        if d < datetime(2025, 12, 20):

            old_adv_url = OLD_ADVANCE.format(date=date_str)

            download(old_adv_url, adv_sum_path)

        # New advance
        else:

            new_sum = NEW_BOX_SUMMARY.format(compact=compact)
            new_det = NEW_BOX_DETAILED.format(compact=compact)

            download(new_sum, adv_sum_path)
            download(new_det, adv_det_path)


if __name__ == "__main__":
    main()

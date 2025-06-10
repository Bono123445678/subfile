import json
import time
import random
import os

MAX_RETRIES = 3

# تحميل الحسابات من account.json
def load_accounts():
    if os.path.exists("account.json"):
        try:
            with open("account.json", "r") as f:
                accounts = json.load(f)
                return accounts
        except Exception as e:
            print(f"[⚠️] Failed to load account.json: {e}")
    return {"reddit": [], "pinterest": []}

# توزيع عشوائي لحساب من نوع معين
def get_random_account(accounts, platform):
    return random.choice(accounts.get(platform, [])) if accounts.get(platform) else None

def simulate_article_visit(url, proxy=None):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            if proxy:
                print(f"[👣][Attempt {attempt}] Visiting {url} using proxy {proxy}")
            else:
                print(f"[👣][Attempt {attempt}] Visiting {url} without proxy")
            time.sleep(random.uniform(2, 5))
            print(f"[✅] Successfully visited {url}")
            return True
        except Exception as e:
            print(f"[❌] Error visiting article (attempt {attempt}): {e}")
            time.sleep(2)
    print(f"[⚠️] Failed to visit {url} after {MAX_RETRIES} attempts")
    return False

def post_to_reddit(article_url, account):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            print(f"[📢][Attempt {attempt}] Reddit post by {account['reddit_username']}: {article_url}")
            time.sleep(random.uniform(1, 3))
            print(f"[✅] Successfully posted on Reddit: {article_url}")
            return True
        except Exception as e:
            print(f"[❌] Reddit posting error (attempt {attempt}): {e}")
            time.sleep(2)
    print(f"[⚠️] Failed to post on Reddit after {MAX_RETRIES} attempts")
    return False

def post_to_pinterest(article_url, account):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            print(f"[📌][Attempt {attempt}] Pinterest post by {account['pinterest_username']}: {article_url}")
            time.sleep(random.uniform(1, 3))
            print(f"[✅] Successfully posted on Pinterest: {article_url}")
            return True
        except Exception as e:
            print(f"[❌] Pinterest posting error (attempt {attempt}): {e}")
            time.sleep(2)
    print(f"[⚠️] Failed to post on Pinterest after {MAX_RETRIES} attempts")
    return False

def run_agent(agent_config, global_accounts):
    proxy = agent_config.get("proxy")
    delay = agent_config.get("delay", 5)
    articles = agent_config.get("articles_to_visit", [])
    platforms = agent_config.get("platforms", [])

    if not articles:
        print("[❌] No articles assigned to this agent.")
        return

    for url in articles:
        if not simulate_article_visit(url, proxy):
            continue

        if "reddit" in platforms:
            reddit_account = get_random_account(global_accounts, "reddit")
            if reddit_account:
                post_to_reddit(url, reddit_account)
            else:
                print("[⚠️] No Reddit account available.")

        if "pinterest" in platforms:
            pinterest_account = get_random_account(global_accounts, "pinterest")
            if pinterest_account:
                post_to_pinterest(url, pinterest_account)
            else:
                print("[⚠️] No Pinterest account available.")

        time.sleep(delay)

def main():
    global_accounts = load_accounts()

    try:
        with open("agent_config.json", "r") as f:
            config = json.load(f)
    except Exception as e:
        print(f"[❌] Failed to load agent_config.json: {e}")
        return

    agents = config.get("agents", [])
    print(f"[ℹ️] Starting {len(agents)} agents...")

    for agent in agents:
        run_agent(agent, global_accounts)

if __name__ == "__main__":
    main()

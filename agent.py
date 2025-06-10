import json
import time
import random

MAX_RETRIES = 3

# محاكاة زيارة مقال مع retry وبروكسي (لو حبيت تستخدمه)
def simulate_article_visit(url, proxy=None):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            if proxy:
                print(f"[👣][Attempt {attempt}] Visiting {url} using proxy {proxy}")
            else:
                print(f"[👣][Attempt {attempt}] Visiting {url} without proxy")
            # هنا ممكن تضيف كود زيارة المقال باستخدام requests مع بروكسي
            # مثلا requests.get(url, proxies=proxy_dict)
            time.sleep(random.uniform(2, 5))  # محاكاة وقت قراءة
            print(f"[✅] Successfully visited {url}")
            return True
        except Exception as e:
            print(f"[❌] Error visiting article (attempt {attempt}): {e}")
            time.sleep(2)  # تأخير قبل إعادة المحاولة
    print(f"[⚠️] Failed to visit {url} after {MAX_RETRIES} attempts")
    return False

# نشر على Reddit مع retry
def post_to_reddit(article_url, account):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            print(f"[📢][Attempt {attempt}] Reddit post by {account['reddit_username']}: {article_url}")
            # أضف هنا كود API النشر على Reddit باستخدام بيانات الحساب
            time.sleep(random.uniform(1, 3))  # محاكاة وقت النشر
            print(f"[✅] Successfully posted on Reddit: {article_url}")
            return True
        except Exception as e:
            print(f"[❌] Reddit posting error (attempt {attempt}): {e}")
            time.sleep(2)
    print(f"[⚠️] Failed to post on Reddit after {MAX_RETRIES} attempts")
    return False

# نشر على Pinterest مع retry
def post_to_pinterest(article_url, account):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            print(f"[📌][Attempt {attempt}] Pinterest post by {account['pinterest_username']}: {article_url}")
            # أضف هنا كود API النشر على Pinterest باستخدام بيانات الحساب
            time.sleep(random.uniform(1, 3))  # محاكاة وقت النشر
            print(f"[✅] Successfully posted on Pinterest: {article_url}")
            return True
        except Exception as e:
            print(f"[❌] Pinterest posting error (attempt {attempt}): {e}")
            time.sleep(2)
    print(f"[⚠️] Failed to post on Pinterest after {MAX_RETRIES} attempts")
    return False

# تنفيذ مهام الوكيل الواحد
def run_agent(agent_config):
    proxy = agent_config.get("proxy")
    account = agent_config.get("account", {})
    delay = agent_config.get("delay", 5)
    articles = agent_config.get("articles_to_visit", [])
    platforms = agent_config.get("platforms", [])

    if not articles:
        print("[❌] No articles assigned to this agent.")
        return

    for url in articles:
        if not simulate_article_visit(url, proxy):
            continue  # تجاهل النشر لو زيارة المقال فشلت

        if "reddit" in platforms:
            post_to_reddit(url, account)

        if "pinterest" in platforms:
            post_to_pinterest(url, account)

        time.sleep(delay)

def main():
    try:
        with open("agent_config.json", "r") as f:
            config = json.load(f)
    except Exception as e:
        print(f"[❌] Failed to load agent_config.json: {e}")
        return

    agents = config.get("agents", [])
    print(f"[ℹ️] Starting {len(agents)} agents...")

    for agent in agents:
        run_agent(agent)

if __name__ == "__main__":
    main()

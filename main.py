import json
import asyncio
from proxy import ProxyManager
from agent import Agent

# قراءة حسابات من ملف JSON
def load_accounts(filepath="account.json"):
    with open(filepath, "r") as f:
        accounts = json.load(f)
    return accounts

async def main():
    # تحميل الحسابات
    accounts = load_accounts()
    print(f"Loaded {len(accounts)} accounts.")

    # إنشاء مدير البروكسيات
    proxy_manager = ProxyManager()

    # اجلب البروكسيات الصالحة من مصادر بروكسي متعددة
    print("Fetching and testing proxies...")
    await proxy_manager.fetch_and_test_proxies()
    valid_proxies = proxy_manager.get_valid_proxies()
    print(f"Valid proxies found: {len(valid_proxies)}")

    # تحديد عدد الAgents المطلوب تشغيلهم
    # مثلاً العدد الأصغر بين حسابات أو بروكسيات عشان ما نتجاوز العدد
    num_agents = min(len(accounts), len(valid_proxies))
    print(f"Running {num_agents} agents...")

    agents = []
    for i in range(num_agents):
        account = accounts[i]
        proxy = valid_proxies[i]
        agent = Agent(account=account, proxy=proxy)
        agents.append(agent)

    # تشغيل كل الAgents بشكل متزامن
    await asyncio.gather(*(agent.run() for agent in agents))

if __name__ == "__main__":
    asyncio.run(main())

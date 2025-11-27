import os
import requests
from datetime import datetime, timedelta

token = os.environ["GITHUB_TOKEN"]
repo = os.environ["GITHUB_REPOSITORY"]
days = int(os.environ.get("RETENTION_DAYS", 7))  # 默认保留 7 天

api_url = f"https://api.github.com/repos/{repo}/actions/caches"
headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {token}"
}

print(f"🔍 获取缓存列表（保留最近 {days} 天）...")

r = requests.get(api_url, headers=headers)
if r.status_code != 200:
    print("❌ 获取缓存失败:", r.text)
    exit(1)

caches = r.json().get("actions_caches", [])
print(f"共发现 {len(caches)} 个缓存")

cutoff = datetime.utcnow() - timedelta(days=days)
deleted = 0

for c in caches:
    cache_id = c["id"]
    key = c["key"]
    created = datetime.strptime(c["created_at"], "%Y-%m-%dT%H:%M:%SZ")

    if created < cutoff:
        print(f"🗑 删除缓存 {cache_id} - key={key} - 创建时间={c['created_at']}")
        del_url = f"{api_url}/{cache_id}"
        d = requests.delete(del_url, headers=headers)

        if d.status_code == 204:
            deleted += 1
        else:
            print("❌ 删除失败:", d.text)

print(f"✨ 清理完成：删除 {deleted} 个缓存")

import requests
from bs4 import BeautifulSoup
import time
import json

# ステップ1：対象ライブラリリスト
libraries = [
    {"group": "org.apache.commons", "artifact": "commons-lang3"},
    {"group": "com.google.guava", "artifact": "guava"}
]

def build_javadoc_url(group_id, artifact_id, version="latest"):
    return f"https://javadoc.io/doc/{group_id}/{artifact_id}/{version}"

def get_class_list(javadoc_base_url):
    index_url = f"{javadoc_base_url}/allclasses-index.html"
    res = requests.get(index_url)
    if res.status_code != 200:
        print(f"[!] Failed to load: {index_url}")
        return []

    soup = BeautifulSoup(res.text, "html.parser")
    links = soup.find_all("a")
    class_infos = []

    for link in links:
        href = link.get("href")
        class_name = link.text.strip()
        if href:
            class_infos.append({
                "class_name": class_name,
                "class_url": javadoc_base_url + "/" + href
            })
    return class_infos

def parse_class_methods(class_url):
    res = requests.get(class_url)
    if res.status_code != 200:
        return []

    soup = BeautifulSoup(res.text, "html.parser")
    methods = []
    tables = soup.find_all("table", class_="memberSummary")
    for table in tables:
        if "Method Summary" in table.text:
            rows = table.find_all("tr")[1:]  # Skip header row
            for row in rows:
                cols = row.find_all("td")
                if len(cols) >= 3:
                    return_type = cols[0].text.strip()
                    method_name = cols[1].text.strip()
                    description = cols[2].text.strip()
                    methods.append({
                        "method_name": method_name,
                        "return_type": return_type,
                        "description": description
                    })
    return methods

# ステップ2〜4：ライブラリごとに処理
output = []

for lib in libraries:
    print(f"Processing {lib['group']}:{lib['artifact']}")
    base_url = build_javadoc_url(lib["group"], lib["artifact"])
    classes = get_class_list(base_url)

    for cls in classes[:5]:  # ← ⚠️上限設定（試験用）
        time.sleep(1)
        methods = parse_class_methods(cls["class_url"])
        output.append({
            "library": f"{lib['group']}:{lib['artifact']}",
            "class_name": cls["class_name"],
            "class_url": cls["class_url"],
            "methods": methods
        })

# 保存
with open("javadoc_dump.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print("✅ Done. Results saved to javadoc_dump.json")

import requests
from bs4 import BeautifulSoup

def search_mvn_repository(lib_name):
    search_url = f"https://mvnrepository.com/search?q={lib_name}"
    res = requests.get(search_url)
    soup = BeautifulSoup(res.text, "html.parser")
    first_result = soup.select_one(".im-title a")
    if not first_result:
        return None
    lib_url = "https://mvnrepository.com" + first_result["href"]
    return extract_coordinates(lib_url)

def extract_coordinates(lib_url):
    res = requests.get(lib_url)
    soup = BeautifulSoup(res.text, "html.parser")
    breadcrumb = soup.select("ul.breadcrumb li a")
    if len(breadcrumb) < 3:
        return None
    group_id = breadcrumb[-2].text.strip()
    artifact_id = breadcrumb[-1].text.strip()
    return group_id, artifact_id

def build_javadoc_url(group_id, artifact_id):
    return f"https://javadoc.io/doc/{group_id}/{artifact_id}"

# 例
lib_name = "mina-core"
coords = search_mvn_repository(lib_name)
if coords:
    group_id, artifact_id = coords
    javadoc_url = build_javadoc_url(group_id, artifact_id)
    print("Javadoc URL:", javadoc_url)
else:
    print("ライブラリが見つかりませんでした")

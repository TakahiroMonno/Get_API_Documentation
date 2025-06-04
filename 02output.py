import requests
import json
import os


### ステップ2: ライブラリ名とバージョンからMaven Central RepositoryのURLを取得し、JARファイルをダウンロード

# JARファイルを保存するディレクトリ
DOWNLOAD_DIR = "downloaded_jars"
os.makedirs(DOWNLOAD_DIR, exist_ok=True) # ディレクトリが存在しない場合は作成

def get_group_id_from_maven_central(artifact_id, version):
    """
    Maven Central Repositoryの検索APIを使ってgroupIdを取得する。
    """
    # mvnrepository.com のAPIエンドポイントを利用（より使いやすいため）
    # プロダクション環境ではrate limitに注意
    search_url = f"[https://search.maven.org/solrsearch/select?q=a%3A%22](https://search.maven.org/solrsearch/select?q=a%3A%22){artifact_id}%22%20AND%20v%3A%22{version}%22&rows=1&wt=json"
    
    print(f"\nMaven CentralでgroupIdを検索中: {search_url}")
    try:
        response = requests.get(search_url, timeout=10) # タイムアウトを設定
        response.raise_for_status()
        search_results = response.json()
        
        # 検索結果からgroupIdを抽出
        if search_results and "response" in search_results and "docs" in search_results["response"]:
            docs = search_results["response"]["docs"]
            if docs:
                return docs[0].get("g") # 'g' キーがgroupId
        print(f"groupIdが見つかりませんでした: artifactId={artifact_id}, version={version}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Maven Central検索中にエラーが発生しました: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Maven CentralのレスポンスがJSONとして解析できませんでした: {e}")
        return None


def get_jar_url(group_id, artifact_id, version):
    """
    groupId, artifactId, versionからMaven CentralのJARダウンロードURLを構築する。
    """
    if not all([group_id, artifact_id, version]):
        return None
    
    # groupIdをパス形式に変換 (例: com.example.myproject -> com/example/myproject)
    group_path = group_id.replace('.', '/')
    
    jar_url = (
        f"[https://repo1.maven.org/maven2/](https://repo1.maven.org/maven2/)"
        f"{group_path}/"
        f"{artifact_id}/"
        f"{version}/"
        f"{artifact_id}-{version}.jar"
    )
    return jar_url

def download_jar(url, save_path):
    """
    指定されたURLからJARファイルをダウンロードする。
    """
    if not url:
        print("ダウンロードURLが指定されていません。")
        return False

    print(f"JARファイルをダウンロード中: {url}")
    try:
        # stream=True で大きなファイルでも効率的にダウンロード
        with requests.get(url, stream=True, timeout=30) as r:
            r.raise_for_status() # HTTPエラーが発生した場合に例外を発生
            with open(save_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): # チャンク単位で書き込み
                    f.write(chunk)
        print(f"JARファイルをダウンロードしました: {save_path}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"JARファイルのダウンロード中にエラーが発生しました: {e}")
        return False
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e}")
        return False

# 抽出した情報があればJARをダウンロード
if extracted_info:
    library_name = extracted_info['name']
    previous_version = extracted_info['previous_version']
    new_version = extracted_info['new_version']

    # 変更前バージョンのJARをダウンロード
    print("\n--- 変更前バージョンのJARダウンロード ---")
    previous_group_id = get_group_id_from_maven_central(library_name, previous_version)
    if previous_group_id:
        previous_jar_url = get_jar_url(previous_group_id, library_name, previous_version)
        previous_jar_save_path = os.path.join(DOWNLOAD_DIR, f"{library_name}-{previous_version}.jar")
        download_jar(previous_jar_url, previous_jar_save_path)
    else:
        print(f"変更前バージョンのgroupIdが見つからないため、JARをダウンロードできませんでした: {library_name}:{previous_version}")

    # 変更後バージョンのJARをダウンロード
    print("\n--- 変更後バージョンのJARダウンロード ---")
    new_group_id = get_group_id_from_maven_central(library_name, new_version)
    if new_group_id:
        new_jar_url = get_jar_url(new_group_id, library_name, new_version)
        new_jar_save_path = os.path.join(DOWNLOAD_DIR, f"{library_name}-{new_version}.jar")
        download_jar(new_jar_url, new_jar_save_path)
    else:
        print(f"変更後バージョンのgroupIdが見つからないため、JARをダウンロードできませんでした: {library_name}:{new_version}")
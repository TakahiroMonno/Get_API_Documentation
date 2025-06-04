#BUMPのJSONファイルからライブラリ名とバージョンを取得

import requests
import json

def get_bump_data_from_github_raw(owner, repo, branch, file_path):
    """
    GitHubのRaw Content URLからJSONファイルの内容を取得する。

    Args:
        owner (str): GitHubユーザー名または組織名
        repo (str): リポジトリ名
        branch (str): ブランチ名 (例: 'main' または 'master')
        file_path (str): リポジトリ内のJSONファイルのパス (例: 'data/bump.json')

    Returns:
        dict: JSONファイルの内容をパースした辞書、またはNone（エラーの場合）
    """
    raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{file_path}"
    
    try:
        response = requests.get(raw_url)
        response.raise_for_status()  # HTTPエラーがあれば例外を発生させる

        bump_data = response.json()
        return bump_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching JSON from GitHub: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None

# 使用例 (適宜、owner, repo, branch, file_pathを置き換えてください)
# 例: 'chains-project/bump' リポジトリの 'main' ブランチにある 'data/benchmark/some_commit_sha.json' を取得する場合
# 実際のBUMPのJSONファイルのパスを確認してください
owner = "chains-project"
repo = "bump"
branch = "main"
file_path = "data/benchmark/your_actual_bump_file.json" # ここを実際のパスに置き換える

bump_json_data = get_bump_data_from_github_raw(owner, repo, branch, file_path)

if bump_json_data:
    print("BUMP JSON データが正常に取得されました:")
    # ここでJSONデータからライブラリ名とバージョンを抽出するロジックを実装
    # bump_json_dataの構造に依存します
    # 例: {'dependencies': [{'name': 'library_A', 'version': '1.0.0'}, ...]} のような場合
    if 'dependencies' in bump_json_data:
        for dep in bump_json_data['dependencies']:
            print(f"  ライブラリ名: {dep.get('name')}, バージョン: {dep.get('version')}")
    else:
        print("JSONの構造が期待と異なります。")
else:
    print("BUMP JSON データの取得に失敗しました。")
    
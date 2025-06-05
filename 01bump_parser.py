import requests
import json

def get_and_extract_bump_info(json_raw_url):
    """
    指定されたGitHub Raw URLからBUMPのJSONファイルをダウンロードし、
    ライブラリ名、変更前後のバージョンを抽出する関数。

    Args:
        json_raw_url (str): GitHub上のBUMP JSONファイルのRaw URL。

    Returns:
        dict: 抽出された情報 {'group_name': str, 'name': str, 'previous_version': str, 'new_version': str}
              またはNone（情報が抽出できなかった場合）
    """
    bump_data = None
    try:
        response = requests.get(json_raw_url)
        response.raise_for_status() # HTTPエラーがあれば例外を発生
        bump_data = response.json()
        print("JSONデータが正常に取得されました。")
    except requests.exceptions.RequestException as e:
        print(f"URLからのデータ取得中にエラーが発生しました: {e}")
        return None # エラーの場合はNoneを返す
    except json.JSONDecodeError as e:
        print(f"取得したデータがJSONとして解析できませんでした: {e}")
        return None # エラーの場合はNoneを返す

    # ここからJSONデータからライブラリ情報を抽出するロジック
    if not bump_data or "updatedDependency" not in bump_data:
        print("JSONデータが不正であるか、'updatedDependency'キーが見つかりません。")
        return None

    updated_dep = bump_data["updatedDependency"]

    if all(k in updated_dep for k in ["dependencyGroupID", "dependencyArtifactID", "previousVersion", "newVersion"]):
        group_name = updated_dep["dependencyGroupID"]
        library_name = updated_dep["dependencyArtifactID"]
        previous_version = updated_dep["previousVersion"]
        new_version = updated_dep["newVersion"]

        return {
            "group_name": group_name,
            "name": library_name,
            "previous_version": previous_version,
            "new_version": new_version
        }
    else:
        print("必要なライブラリまたはバージョン情報が'updatedDependency'内に見つかりません。")
        return None

# このファイルが直接実行された場合にのみテストコードを実行するブロック
if __name__ == "__main__":
    test_json_url = "https://raw.githubusercontent.com/chains-project/bump/refs/heads/main/data/benchmark/00a7cc31784ac4a9cc27d506a73ae589d6df36d6.json"
    extracted_info = get_and_extract_bump_info(test_json_url)

    if extracted_info:
        print("\n--- bump_parser.py から抽出されたライブラリ情報 (テスト実行) ---")
        print(f"  グループ名: {extracted_info['group_name']}")
        print(f"  ライブラリ名: {extracted_info['name']}")
        print(f"  変更前バージョン: {extracted_info['previous_version']}")
        print(f"  変更後バージョン: {extracted_info['new_version']}")
    else:
        print("--- bump_parser.py で情報の抽出に失敗しました (テスト実行) ---")
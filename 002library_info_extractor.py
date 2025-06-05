# JSONから特定の要素を抽出するモジュール

# JSONデータからライブラリ名、変更前後のバージョンを取得する関数
def extract_library_and_versions(json_data):
    """
    Args:
        json_data (dict): Pythonの辞書オブジェクトに変換されたJSONデータ。

    Returns:
        dict: 抽出された情報 {'group_name': str, 'library_name': str, 'previous_version': str, 'new_version': str}
              またはNone（情報が抽出できなかった場合）。
    """
    if not json_data or "updatedDependency" not in json_data:
        print("JSONデータが不正であるか、'updatedDependency'キーが見つかりません。")
        return None

    updated_dep = json_data["updatedDependency"]

    if all(k in updated_dep for k in ["dependencyGroupID", "dependencyArtifactID", "previousVersion", "newVersion"]):
        group_name = updated_dep["dependencyGroupID"]
        library_name = updated_dep["dependencyArtifactID"]
        previous_version = updated_dep["previousVersion"]
        new_version = updated_dep["newVersion"]

        return {
            "group_name": group_name,
            "library_name": library_name,
            "previous_version": previous_version,
            "new_version": new_version
        }
    else:
        print("必要なライブラリまたはバージョン情報が'updatedDependency'内に見つかりません。")
        return None

# このファイルが直接実行された場合にのみテストコードを実行するブロック
if __name__ == "__main__":
    print("--- library_info_extractor.py を直接実行しています（テストモード） ---")
    # テスト用のダミーJSONデータ（実際にはjson_downloaderから来るデータ）
    dummy_json_data = {
      "url" : "https://github.com/quickfix-j/quickfixj/pull/502",
      "project" : "quickfixj",
      "updatedDependency" : {
        "dependencyGroupID" : "org.apache.mina",
        "dependencyArtifactID" : "mina-core",
        "previousVersion" : "2.1.5",
        "newVersion" : "2.2.1"
      }
    }
    extracted_info = extract_library_and_versions(dummy_json_data)

    if extracted_info:
        print("\n抽出されたライブラリ情報:")
        print(f"  グループ名: {extracted_info['group_name']}")
        print(f"  ライブラリ名: {extracted_info['library_name']}")
        print(f"  変更前バージョン: {extracted_info['previous_version']}")
        print(f"  変更後バージョン: {extracted_info['new_version']}")
    else:
        print("情報の抽出に失敗しました。")
    print("--- テスト実行終了 ---")
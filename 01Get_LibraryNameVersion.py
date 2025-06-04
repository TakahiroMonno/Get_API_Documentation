#BUMPのJSONファイルからライブラリ名とバージョンを取得
import requests
import json

# JSONファイルをダウンロード
# 特定のJSONファイルのRaw URLを貼り付け
json_raw_url = "https://raw.githubusercontent.com/chains-project/bump/refs/heads/main/data/benchmark/00a7cc31784ac4a9cc27d506a73ae589d6df36d6.json" 

#　エラーハンドリングでプログラムの堅牢性を高める
try: #try-exceptブロック
    # URLにGETリクエストを送信＆レスポンス取得
    response = requests.get(json_raw_url)
    
    # HTTPステータスコードが200番台（成功）でなければ例外を発生させる（例: 404 Not Found, 500 Internal Server Error など）
    response.raise_for_status() 
    
    # レスポンスボディをJSONとして解析し、辞書に変換（BUMPのJSONが{}型のため）
    bump_data = response.json() #　取得したJSONの格納
    
    print("JSONデータが正常に取得されました。")
    # 取得したJSONを試しに表示
    # print(json.dumps(bump_data, indent=2)) # きれいに表示したい場合はjsonモジュールも必要
    
except requests.exceptions.RequestException as e:
    # HTTPリクエスト関連のエラー（ネットワーク接続の問題、URL間違いなど）
    print(f"URLからのデータ取得中にエラーが発生しました: {e}")
    bump_data = None # エラーの場合
except json.JSONDecodeError as e:
    # 取得した内容がJSONとして不正な場合のエラー
    print(f"取得したデータがJSONとして解析できませんでした: {e}")
    bump_data = None
    
# JSONファイルからライブラリ名とバージョンを抽出する関数を定義
def extract_library_and_versions(json_data): 
    """ # ドキュメント文字列
    JSONデータからライブラリ名、変更前後のバージョンを抽出する関数

    Args: # 引数の説明
        json_data (dict): parseして辞書オブジェクトに変換されたJSON

    Returns: # 戻り値の説明（辞書かNoneで返す）
        dict: JSONから抽出した情報 {'name': str, 'previous_version': str, 'new_version': str}
              またはNone（情報が抽出できなかった場合）
    """ #どちらの戻り値を返すかで条件分岐
    if not json_data or "updatedDependency" not in json_data:
        print("JSONデータが不正であるか、'updatedDependency'キーが見つかりません。")
        return None

    # 'updatedDependency'キーのみを抽出
    updated_dep = json_data["updatedDependency"]

    # 必要なキーが存在するか確認する（安全な抽出のため）
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

# 抽出した情報を格納（グループ名、ライブラリ名、変更前＆後バージョン）
extracted_info = extract_library_and_versions(bump_data)

if extracted_info:
    print("\n抽出されたライブラリ情報:")
    print(f"  グループ名: {extracted_info['group_name']}")
    print(f"  ライブラリ名: {extracted_info['name']}")
    print(f"  変更前バージョン: {extracted_info['previous_version']}")
    print(f"  変更後バージョン: {extracted_info['new_version']}")
else:
    print("情報の抽出に失敗しました。")
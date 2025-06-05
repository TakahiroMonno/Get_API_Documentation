# BUMPのJSONファイルをダウンロードする
# 指定されたURLからJSONデータをダウンロードし、辞書型に変換するモジュール
import requests
import json

# JSONデータをダウンロードして辞書型に変換する関数
def download_json_from_url(json_raw_url):
    """
    Args:
        json_raw_url (str): ダウンロードするJSONファイルのURL。

    Returns:
        dict: ダウンロードしてパースされたJSONデータ（辞書）、
              またはNone（ダウンロードやパースに失敗した場合）。
    """
    try: # try-exceptブロックでエラーハンドリング
        response = requests.get(json_raw_url)
        response.raise_for_status() # HTTPエラーがあれば例外を発生

        bump_data = response.json()
        print(f"JSONデータが正常にダウンロードされました: {json_raw_url}")
        return bump_data
        
    except requests.exceptions.RequestException as e:
        print(f"URLからのデータダウンロード中にエラーが発生しました: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"ダウンロードしたデータがJSONとして解析できませんでした: {e}")
        return None


# モジュールとして独立＆テスト実行のブロック（Pythonモジュールの慣習）
if __name__ == "__main__": #mina-coreでテスト
    test_url = "https://raw.githubusercontent.com/chains-project/bump/refs/heads/main/data/benchmark/00a7cc31784ac4a9cc27d506a73ae589d6df36d6.json"
    print("--- json_downloader.py を直接実行しています（テストモード） ---")
    downloaded_data = download_json_from_url(test_url)
    if downloaded_data:
        print("\nダウンロードされたJSONデータのキー（一部）:")
        print(list(downloaded_data.keys())[:5]) # 最初の5つのキーを表示
    else:
        print("JSONデータのダウンロードに失敗しました。")
    print("--- テスト実行終了 ---")
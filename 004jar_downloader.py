# 004 MVCRのURLから変更前後のJARファイルを取得するモジュール
import requests
import os

# URLからファイルをダウンロードするヘルパー関数(モジュール内で利用)
def _download_single_file(url, save_path):
    """
    Args:
        url (str): ダウンロードするファイルのURL。
        save_path (str): ファイルを保存するローカルパス。

    Returns:
        bool: ダウンロードが成功した場合はTrue、失敗した場合はFalse。
    """
    print(f"ダウンロード開始: {url} へ")
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status() # HTTPエラーがあれば例外を発生
            with open(save_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"ダウンロード完了: {save_path}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"ダウンロード中にエラーが発生しました: {e}")
        return False
    except IOError as e:
        print(f"ファイルの保存中にエラーが発生しました: {e}")
        return False

# 指定されたURLから変更前後のJARファイルをダウンロードし、ローカルパスを返す関数(_download_single_file関数を内部的に利用)
def download_jar_files(previous_jar_url, new_jar_url, artifact_id, previous_version, new_version, download_dir="downloaded_jars"):
    """
    Args:
        previous_jar_url (str): 変更前のJARファイルのダウンロードURL。
        new_jar_url (str): 変更後のJARファイルのダウンロードURL。
        artifact_id (str): ライブラリのアーティファクトID（ファイル名に使用）。
        previous_version (str): 変更前のバージョン（ファイル名に使用）。
        new_version (str): 変更後のバージョン（ファイル名に使用）。
        download_dir (str): JARファイルを保存するローカルディレクトリ名（デフォルト: 'downloaded_jars'）。

    Returns:
        tuple: (previous_jar_path, new_jar_path) - ダウンロードしたJARファイルのローカルパスのタプル。
               ダウンロードに失敗した場合は (None, None)。
    """
    # 保存先ディレクトリの作成 (もし存在しなければ)
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
        print(f"ディレクトリを作成しました: {download_dir}")

    # 各JARファイルの保存パスを構築
    previous_jar_path = os.path.join(download_dir, f"{artifact_id}-{previous_version}.jar")
    new_jar_path = os.path.join(download_dir, f"{artifact_id}-{new_version}.jar")

    download_success_pre = False
    download_success_new = False

    print(f"\n--- 変更前バージョンJARダウンロード ---")
    download_success_pre = _download_single_file(previous_jar_url, previous_jar_path)

    print(f"\n--- 変更後バージョンJARダウンロード ---")
    download_success_new = _download_single_file(new_jar_url, new_jar_path)

    if download_success_pre and download_success_new:
        print("\n両方のJARファイルのダウンロードに成功しました。")
        return (previous_jar_path, new_jar_path)
    else:
        print("\nJARファイルのダウンロードに失敗したか、一部成功しました。")
        return (None, None)

# このファイルが直接実行された場合にのみテストコードを実行するブロック
if __name__ == "__main__":
    print("--- jar_downloader.py を直接実行しています（テストモード） ---")
    
    # テスト用のダミー情報
    test_artifact_id = "mina-core"
    test_previous_version = "2.1.5"
    test_new_version = "2.2.1"
    
    # ダミーのダウンロードURL (実際にはmaven_url_builderから取得)
    # これらは実際に存在するURLである必要があります
    test_previous_url = "https://repo1.maven.org/maven2/org/apache/mina/mina-core/2.1.5/mina-core-2.1.5.jar"
    test_new_url = "https://repo1.maven.org/maven2/org/apache/mina/mina-core/2.2.1/mina-core-2.2.1.jar"
    
    # JARファイルをダウンロード
    jar_paths = download_jar_files(
        test_previous_url, test_new_url,
        test_artifact_id, test_previous_version, test_new_version,
        download_dir="test_jars" # テスト用に別のディレクトリを指定
    )

    if jar_paths[0] and jar_paths[1]:
        print("\n--- JARダウンロードテスト結果 ---")
        print(f"旧JARパス: {jar_paths[0]}")
        print(f"新JARパス: {jar_paths[1]}")
    else:
        print("\n--- JARダウンロードテスト結果 ---")
        print("JARダウンロードテストに失敗しました。")
    print("--- テスト実行終了 ---")
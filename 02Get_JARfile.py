#Maven Central RepositoryからJARファイルをダウンロード
import requests
import json
import os

# JARファイルを格納するディレクトリ
DOWNLOAD_DIR = "downloaded_jars"

# JARファイルのURLを構築
# Maven Central RepositoryのベースURL
MAVEN_BASE_URL = "https://repo1.maven.org/maven2/"

# MVCRからJARファイルのURLを取得する関数
def get_maven_jar_url(group_id, artifact_id, version):
    """
    Args:　引数
        group_id (str): (例: 'org.apache.mina')
        artifact_id (str): (例: 'mina-core')
        version (str): (例: '2.1.5')

    Returns:　戻り値
        str: JARファイルのダウンロードURL
    """
    # グループIDをパス形式に変換 (例: org.apache.mina -> org/apache/mina)
    group_path = group_id.replace('.', '/')
    
    # URLを構築
    jar_url = f"{MAVEN_BASE_URL}{group_path}/{artifact_id}/{version}/{artifact_id}-{version}.jar"
    return jar_url #JARファイルのURLを返す

# JARファイルをダウンロードし、保存する関数
def download_file(url, save_path):
    """
    Args:
        url (str): ダウンロードするファイルのURL
        save_path (str): ファイルを保存するローカルパス

    Returns:
        bool: ダウンロードが成功した場合はTrue、失敗した場合はFalse
    """
    print(f"ダウンロード開始: {url} へ")
    try:
        # ストリーミングダウンロードで大きなファイルにも対応
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

# --- ここからが、抽出した情報を使ったJARダウンロードのメインロジック ---

# extracted_info は、前のステップで抽出された情報（辞書）
if extracted_info:
    group_id = extracted_info['group_name']
    artifact_id = extracted_info['name']
    previous_version = extracted_info['previous_version']
    new_version = extracted_info['new_version']

    # 保存先ディレクトリの作成 (例: 'downloaded_jars' フォルダ)
    download_dir = "downloaded_jars"
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
        print(f"ディレクトリを作成しました: {download_dir}")

    # 変更前バージョンのJARファイルをダウンロード
    previous_jar_url = get_maven_jar_url(group_id, artifact_id, previous_version)
    previous_jar_path = os.path.join(download_dir, f"{artifact_id}-{previous_version}.jar")
    print(f"\n変更前バージョンJARダウンロード:")
    download_success_pre = download_file(previous_jar_url, previous_jar_path)

    # 変更後バージョンのJARファイルをダウンロード
    new_jar_url = get_maven_jar_url(group_id, artifact_id, new_version)
    new_jar_path = os.path.join(download_dir, f"{artifact_id}-{new_version}.jar")
    print(f"\n変更後バージョンJARダウンロード:")
    download_success_new = download_file(new_jar_url, new_jar_path)

    if download_success_pre and download_success_new:
        print("\n両方のJARファイルのダウンロードに成功しました。")
        print(f"旧JARパス: {previous_jar_path}")
        print(f"新JARパス: {new_jar_path}")
    else:
        print("\nJARファイルのダウンロードに失敗したか、一部成功しました。")
else:
    print("ライブラリ情報が抽出できなかったため、JARファイルのダウンロードはスキップします。")
# JARファイルのダウンロード（URLを用いてローカルに保存）


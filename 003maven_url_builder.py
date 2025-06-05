# ライブラリ名とバージョンより、Maven Central RepositoryのURLを構築するモジュール

# Maven Central RepositoryのベースURLを定数として定義
MAVEN_BASE_URL = "https://repo1.maven.org/maven2/"

#  Maven Central RepositoryのJARファイルダウンロードURLを構築する関数
def get_maven_jar_url(group_id, artifact_id, version):
    """
    Args:
        group_id (str): ライブラリのグループID (例: 'org.apache.mina')
        artifact_id (str): ライブラリのアーティファクトID (例: 'mina-core')
        version (str): ライブラリのバージョン (例: '2.1.5')

    Returns:
        str: JARファイルのダウンロードURL。
    """
    # グループIDをパス形式に変換 (例: org.apache.mina -> org/apache/mina)
    group_path = group_id.replace('.', '/')
    
    # URLを構築
    jar_url = f"{MAVEN_BASE_URL}{group_path}/{artifact_id}/{version}/{artifact_id}-{version}.jar"
    return jar_url

# このファイルが直接実行された場合にのみテストコードを実行するブロック
if __name__ == "__main__":
    print("--- maven_url_builder.py を直接実行しています（テストモード） ---")
    
    # テスト用のダミー情報
    test_group_id = "org.apache.mina"
    test_artifact_id = "mina-core"
    test_version = "2.2.1"
    
    # URLを構築
    built_url = get_maven_jar_url(test_group_id, test_artifact_id, test_version)
    
    print(f"\n構築されたJARダウンロードURL: {built_url}")
    
    # 別の例
    test_group_id_2 = "com.google.guava"
    test_artifact_id_2 = "guava"
    test_version_2 = "32.1.3-jre"
    built_url_2 = get_maven_jar_url(test_group_id_2, test_artifact_id_2, test_version_2)
    print(f"別の構築されたJARダウンロードURL: {built_url_2}")

    print("--- テスト実行終了 ---")
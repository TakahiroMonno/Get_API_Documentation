import requests # HTTPリクエストを送信するためのライブラリをインポート
from bs4 import BeautifulSoup # HTML/XMLをパースしてデータを抽出するためのライブラリをインポート
import time # 時間関連の関数（ここでは遅延処理）をインポート
import json # JSONデータのエンコード/デコードを行うためのライブラリをインポート

# ステップ1：対象ライブラリリストの定義
# スクリプトがAPIドキュメントを収集する対象のJavaライブラリを辞書のリストとして定義します。
# 各辞書はMavenのGroupIdとArtifactIdを含みます。
libraries = [
    {"group": "org.apache.mina", "artifact": "mina-core"},
    {"group": "io.jenkins.tools.bom", "artifact": "bom-2.289.x"}
]

def build_javadoc_url(group_id, artifact_id, version="latest"):
    """
    Maven Central RepositoryでホストされているJavadocのベースURLを構築します。
    javadoc.io を利用して、指定されたGroupId、ArtifactId、バージョンからURLを生成します。
    """
    return f"https://javadoc.io/doc/{group_id}/{artifact_id}/{version}"

def get_class_list(javadoc_base_url):
    """
    指定されたJavadocのベースURLから、すべてのクラスのリストとそのURLを抽出します。
    通常、Javadocの 'allclasses-index.html' ページから情報を取得します。
    """
    index_url = f"{javadoc_base_url}/allclasses-index.html" # 全クラスのインデックスページのURLを構築
    res = requests.get(index_url) # HTTP GETリクエストを送信

    # ステータスコードが200（成功）でなければエラーメッセージを出力し、空のリストを返す
    if res.status_code != 200:
        print(f"[!] Failed to load: {index_url}")
        return []

    soup = BeautifulSoup(res.text, "html.parser") # 取得したHTMLコンテンツをBeautifulSoupでパース
    links = soup.find_all("a") # ページ内のすべての<a>（アンカー）タグを見つける
    class_infos = [] # クラス情報を格納するリストを初期化

    # 各リンクをループ処理し、クラス名とURLを抽出
    for link in links:
        href = link.get("href") # <a>タグのhref属性（リンク先）を取得
        class_name = link.text.strip() # <a>タグのテキストコンテンツ（クラス名）を取得し、前後の空白を除去
        if href: # hrefが存在する場合のみ処理
            class_infos.append({
                "class_name": class_name,
                "class_url": javadoc_base_url + "/" + href # クラスの絶対URLを構築
            })
    return class_infos # 抽出したクラス情報のリストを返す

def parse_class_methods(class_url):
    """
    特定のクラスのJavadocページからメソッド情報を抽出します。
    メソッド名、戻り値の型、説明などを取得します。
    """
    res = requests.get(class_url) # クラスのJavadocページにHTTP GETリクエストを送信

    # ステータスコードが200でなければ空のリストを返す
    if res.status_code != 200:
        return []

    soup = BeautifulSoup(res.text, "html.parser") # 取得したHTMLコンテンツをBeautifulSoupでパース
    methods = [] # メソッド情報を格納するリストを初期化
    tables = soup.find_all("table", class_="memberSummary") # CSSクラスが 'memberSummary' のすべての<table>タグを見つける

    # 各テーブルをループ処理
    for table in tables:
        # テーブルのテキスト内に "Method Summary" が含まれているか確認
        # これにより、メソッドの概要テーブルを特定します。
        if "Method Summary" in table.text:
            rows = table.find_all("tr")[1:]  # ヘッダー行をスキップして、データ行のみを取得
            for row in rows: # 各行をループ処理
                cols = row.find_all("td") # 行内のすべての<td>（テーブルデータ）タグを見つける
                if len(cols) >= 3: # 少なくとも3つの列があるか確認（戻り値の型、メソッド名、説明）
                    return_type = cols[0].text.strip() # 最初の列から戻り値の型を抽出
                    method_name = cols[1].text.strip() # 2番目の列からメソッド名を抽出
                    description = cols[2].text.strip() # 3番目の列から説明を抽出
                    methods.append({
                        "method_name": method_name,
                        "return_type": return_type,
                        "description": description
                    })
    return methods # 抽出したメソッド情報のリストを返す

# ステップ2〜4：ライブラリごとに処理を実行
output = [] # 全ての抽出結果を格納する最終的なリスト

# 定義された各ライブラリをループ処理
for lib in libraries:
    print(f"Processing {lib['group']}:{lib['artifact']}") # 現在処理中のライブラリ名を出力

    # ライブラリのJavadocベースURLを構築
    base_url = build_javadoc_url(lib["group"], lib["artifact"])
    # そのライブラリのすべてのクラスのリストを取得
    classes = get_class_list(base_url)

    # 取得したクラスのリストをループ処理
    # ⚠️上限設定（試験用）：ここでは、各ライブラリから最初の5つのクラスのみを処理します。
    # 全てのクラスを処理する場合は、`[:5]` を削除してください。
    for cls in classes[:5]: 
        time.sleep(1) # サーバーへの負荷を軽減するため、各リクエスト間に1秒の遅延を入れる
        
        # 現在のクラスのメソッド情報をパースして取得
        methods = parse_class_methods(cls["class_url"])
        
        # 抽出した情報をoutputリストに追加
        output.append({
            "library": f"{lib['group']}:{lib['artifact']}", # ライブラリ名
            "class_name": cls["class_name"], # クラス名
            "class_url": cls["class_url"], # クラスのJavadoc URL
            "methods": methods # 抽出されたメソッドのリスト
        })

# 最終結果をJSONファイルとして保存
# ファイル名: javadoc_dump.json
# エンコーディング: UTF-8（日本語などの文字も正しく保存するため）
# インデント: 2（読みやすいように整形）
# ensure_ascii=False: 非ASCII文字をエスケープせずに直接書き込む
with open("javadoc_dump.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print("✅ Done. Results saved to javadoc_dump.json") # 処理完了メッセージ
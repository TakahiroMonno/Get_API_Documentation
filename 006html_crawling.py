import os
from bs4 import BeautifulSoup

def extract_changed_apis_from_html_report(html_report_path):
    """
    japicmpのHTML差分レポートから、変更されたAPIの情報を抽出する関数。

    Args:
        html_report_path (str): japicmpによって生成されたHTMLレポートファイルのパス。

    Returns:
        list: 各要素が変更されたAPIを表す辞書（例: {'type': 'MODIFIED', 'api_signature': 'public void someMethod(String arg)'}）のリスト。
              レポートが見つからない場合や解析に失敗した場合は空のリストを返す。
    """
    if not os.path.exists(html_report_path):
        print(f"エラー: レポートファイルが見つかりません: {html_report_path}")
        return []

    changed_apis = []

    try:
        with open(html_report_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        soup = BeautifulSoup(html_content, 'html.parser')

        # Japicmpレポートの変更要素の一般的な構造を仮定します。
        # これはレポートのHTMLソースを確認して調整する必要があるかもしれません。
        # よくある例: <div>タグに特定のクラス（例: 'modified-api', 'added-api', 'removed-api'）が付いている
        # または、見出し（h3, h4など）が変更タイプを示している場合など。

        # ここでは、変更されたクラスやメソッドが特定のCSSクラスを持つ要素内に表示されると仮定します。
        # 実際には、`japicmp` のHTML構造をブラウザの開発者ツールで確認し、正確なセレクタを特定する必要があります。

        # 例1: 変更タイプを示すクラス名が付いている場合（これは一般的なパターンです）
        # <div class="added">...</div>
        # <div class="removed">...</div>
        # <div class="modified">...</div>
        # <div class="api-signature">public void someMethod(...)</div> など

        # Japicmpのデフォルトレポートでは、以下のような構造が考えられます（バージョンによって異なります）:
        # <div class="diff-container">
        #   <div class="api-diff-entry added">...<span class="signature">...</span>...</div>
        #   <div class="api-diff-entry removed">...<span class="signature">...</span>...</div>
        #   <div class="api-diff-entry modified">...<span class="signature">...</span>...</div>
        # </div>

        # 以下は、Japicmpレポートの一般的な構造を推測したものです。
        # あなたのレポートのHTMLソースを見て、正確なclass名やtagを特定してください。
        
        # 変更タイプごとのエントリを探す
        # 'ADDED', 'REMOVED', 'MODIFIED' の各変更タイプに対応する要素を識別
        # 実際のclass名はブラウザの開発者ツールで確認してください。
        # ここでは 'api-added', 'api-removed', 'api-modified' を仮定します。
        # または、単に 'diff-entry' のような共通クラスで全てを取得し、内部のテキストで判断する場合もあります。

        # 仮のクラス名:
        modified_entries = soup.find_all(class_='modified')
        added_entries = soup.find_all(class_='added')
        removed_entries = soup.find_all(class_='removed')

        # 各エントリからAPIシグネチャを抽出
        for entry in modified_entries:
            # signatureのテキストを抽出する。HTML構造によってパスは変わります。
            # 例: <span class="signature">public void someMethod()</span>
            signature_span = entry.find(class_='signature') # もしsignatureクラスがあれば
            api_signature = signature_span.get_text(strip=True) if signature_span else entry.get_text(strip=True)
            changed_apis.append({'type': 'MODIFIED', 'api_signature': api_signature})

        for entry in added_entries:
            signature_span = entry.find(class_='signature')
            api_signature = signature_span.get_text(strip=True) if signature_span else entry.get_text(strip=True)
            changed_apis.append({'type': 'ADDED', 'api_signature': api_signature})

        for entry in removed_entries:
            signature_span = entry.find(class_='signature')
            api_signature = signature_span.get_text(strip=True) if signature_span else entry.get_text(strip=True)
            changed_apis.append({'type': 'REMOVED', 'api_signature': api_signature})

        # もし変更タイプが特定のセクション見出しの下に全て列挙されている場合：
        # 例えば <h3>Added Classes</h3> の次にリストがある場合など
        # sections = soup.find_all(['h3', 'h4'])
        # for section in sections:
        #     if "Added Classes" in section.get_text():
        #         # そのセクションに続くAPIリストを抽出するロジック
        #         pass

    except Exception as e:
        print(f"HTMLレポートの解析中にエラーが発生しました: {e}")
        return []

    return changed_apis

# --- 実行例 ---
if __name__ == "__main__":
    # ここに、japicmpで生成されたHTMLレポートのパスを指定してください
    report_file = "api_diff_reports/mina-core-2.1.5-vs-mina-core-2.2.1-diff-report.html"

    print(f"レポートファイル '{report_file}' から変更されたAPIを抽出中...")
    extracted_apis = extract_changed_apis_from_html_report(report_file)

    if extracted_apis:
        print("\n--- 抽出された変更API ---")
        for api in extracted_apis:
            print(f"タイプ: {api['type']}, シグネチャ: {api['api_signature']}")
    else:
        print("変更されたAPIは抽出されませんでした。レポートファイルが存在しないか、HTML構造が異なる可能性があります。")
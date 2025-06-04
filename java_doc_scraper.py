# pip install requests beautifulsoup4

import requests
from bs4 import BeautifulSoup
import time
import re

def get_java_doc_url(group_id, artifact_id):
    """
    Maven Central RepositoryのウェブサイトからJavaライブラリのJavadoc URLを探します。
    """
    search_url = f"https://mvnrepository.com/artifact/{group_id}/{artifact_id}"
    print(f"Searching Maven Central for Javadoc URL: {search_url}")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status() # HTTPエラーが発生した場合に例外を発生させる
        
        soup = BeautifulSoup(response.text, 'html.parser')

        # Javadocリンクを探す
        # mvnrepository.comでは、通常 "External Links" セクションにJavadocリンクがある
        # または、ライブラリのページ内に直接 "Javadoc" というテキストを持つリンクがある
        javadoc_link = None

        # 1. "External Links" セクションを探す
        external_links_div = soup.find('div', class_='external-links')
        if external_links_div:
            # リンクテキストが "Javadoc" またはURLに "javadoc" を含むものを探す
            links = external_links_div.find_all('a', href=True)
            for link in links:
                if "javadoc" in link.get_text().lower() or "javadoc" in link['href'].lower():
                    javadoc_link = link['href']
                    break
        
        # 2. 上記で見つからない場合、一般的なページ内のリンクをもう少し広く探す
        if not javadoc_link:
            links = soup.find_all('a', href=True)
            for link in links:
                if "javadoc" in link.get_text().lower() or "javadoc" in link['href'].lower():
                    # 絶対URLに変換
                    if not link['href'].startswith('http'):
                        # 相対URLの場合の基本的な処理 (ドメインがmvnrepository.comでないことを確認するロジックは省略)
                        javadoc_link = requests.compat.urljoin(search_url, link['href'])
                    else:
                        javadoc_link = link['href']
                    break

        if javadoc_link:
            print(f"Found Javadoc URL: {javadoc_link}")
            return javadoc_link
        else:
            print("No explicit Javadoc link found on the page. Trying homepage as fallback.")
            # Javadocリンクが見つからない場合、ホームページリンクを試す
            homepage_link = None
            homepage_a = soup.find('a', class_='url') # 例: <a class="url" href="...">
            if homepage_a and homepage_a.get('href'):
                homepage_link = homepage_a['href']
            
            if homepage_link:
                print(f"Found Homepage URL as fallback: {homepage_link}")
                # ホームページURLからドキュメントを探すのはさらに複雑なので、
                # この関数ではここで終了し、呼び出し元で追加処理が必要
                return homepage_link
            else:
                print("No homepage link found either.")
                return None

    except requests.exceptions.RequestException as e:
        print(f"Error accessing {search_url}: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while searching for Javadoc URL: {e}")
        return None

def get_html_content(url):
    """
    指定されたURLからHTMLコンテンツを取得し、主なテキストを抽出します。
    Javadocは通常、構造が似ているため、一般的なヘッダーとコンテンツタグを対象とします。
    """
    print(f"\nAttempting to fetch content from Javadoc URL: {url}")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status() # HTTPエラーが発生した場合に例外を発生させる

        if 'text/html' not in response.headers.get('Content-Type', ''):
            print(f"Content-Type is not HTML: {response.headers.get('Content-Type')}")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')
        print("Content fetched successfully. Attempting to extract main text from Javadoc.")

        # Javadocのメインコンテンツは通常、<body>タグ内または特定のdiv/articleタグにあります。
        # ここでは、<body>タグの直接の子要素からナビゲーションなどを除いたテキストを抽出します。
        # Javadocの典型的な構造を考慮し、<body>タグ内の<div class="contentContainer">などを探すことが多い
        
        main_content_div = soup.find('div', class_=['contentContainer', 'description'])
        if not main_content_div:
            # 汎用的な方法としてbodyタグ全体を対象にするが、不要な要素を削除する
            main_content_div = soup.body

        if main_content_div:
            # 不要なタグやクラスを除去する（例：ナビゲーション、フッター、広告など）
            for unwanted_tag in main_content_div.find_all(['nav', 'footer', 'header', 'aside', 'script', 'style']):
                unwanted_tag.decompose() # 要素をHTMLから削除

            # <dl>, <dt>, <dd> (定義リスト)などのJavadoc特有の構造を考慮してテキストを整形
            # 例えば、<dt> と <dd> の内容を結合するなど
            
            # get_text() でテキストを抽出し、余分な空白を整形
            text = main_content_div.get_text(separator='\n', strip=True)
            
            # 複数の改行を一つにまとめる
            text = re.sub(r'\n\s*\n', '\n\n', text)
            return text
        else:
            print("Could not find main content div in Javadoc.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching content from {url}: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while processing Javadoc content: {e}")
        return None

def main():
    print("--- Java Library API Documentation Scraper ---")
    group_id = input("Enter Java library Group ID (e.g., org.springframework): ")
    artifact_id = input("Enter Java library Artifact ID (e.g., spring-webmvc): ")

    # ドキュメントURLの取得
    javadoc_url = get_java_doc_url(group_id, artifact_id)

    if javadoc_url:
        print(f"\nPotential Javadoc URL found: {javadoc_url}")
        
        # 少し待ってからコンテンツ取得
        time.sleep(2) 
        
        # Javadocコンテンツの取得と表示
        content = get_html_content(javadoc_url)
        if content:
            print("\n--- Extracted Javadoc Content (Partial Preview) ---")
            # 最初の1000文字だけ表示（長すぎると大変なため）
            print(content[:1000] + "..." if len(content) > 1000 else content)
            print("\n--- End of Content ---")
        else:
            print("Failed to retrieve or parse Javadoc content.")
    else:
        print("Could not find a Javadoc URL for the specified library.")

if __name__ == "__main__":
    main()
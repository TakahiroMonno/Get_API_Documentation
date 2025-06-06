# 005 ローカルJARファイルのAPI差分をjapicmpで分析するモジュール
import subprocess # JapicmpWrapperが内部で使用
import os         

# japicmp_wrapper.py から JapicmpWrapper クラスをインポート
from japicmp_wrapper import JapicmpWrapper

# japicmpで2つのJARファイルのAPI差分を分析し、HTMLレポートを生成する関数
def analyze_api_diff(old_jar_path, new_jar_path, japicmp_jar_path=None, output_dir="api_diff_reports"):
    """
    Args:
        old_jar_path (str): 比較対象の古いJARファイルのローカルパス。
        new_jar_path (str): 比較対象の新しいJARファイルのローカルパス。
        japicmp_jar_path (str, optional): japicmpツール本体のJARファイルのローカルパス。
                                          指定がない場合はJapicmpWrapperが環境変数やカレントディレクトリから探す。
        output_dir (str): レポートを保存するディレクトリ名（デフォルト: 'api_diff_reports'）。

    Returns:
        str: 生成されたHTMLレポートファイルのパス、またはNone（分析に失敗した場合）。
    """
    # JARファイルの存在チェック (JapicmpWrapperの内部でも行われるが、早めにチェックする)
    if not os.path.exists(old_jar_path):
        print(f"エラー: 古いJARファイルが見つかりません: {old_jar_path}")
        return None
    if not os.path.exists(new_jar_path):
        print(f"エラー: 新しいJARファイルが見つかりません: {new_jar_path}")
        return None
    # japicmp_jar_pathの存在チェックはJapicmpWrapperの__init__に任せる

    # レポート保存先ディレクトリの作成
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"レポート出力ディレクトリを作成しました: {output_dir}")

    # 出力レポートファイル名 (例: old-new-diff-report.html)
    old_jar_name = os.path.basename(old_jar_path).replace('.jar', '')
    new_jar_name = os.path.basename(new_jar_path).replace('.jar', '')
    report_filename = f"{old_jar_name}-vs-{new_jar_name}-diff-report.html"
    output_report_path = os.path.join(output_dir, report_filename)

    print(f"\njapicmpラッパーを使ってAPI差分分析を実行中...")

    try:
        # JapicmpWrapperのインスタンスを作成
        # japicmp_jar_pathがNoneの場合、Wrapperが環境変数やカレントディレクトリから探す
        wrapper = JapicmpWrapper(jar_path=japicmp_jar_path)
        
        # JapicmpWrapperのcompareメソッドを呼び出す
        # **kwargsを使ってjapicmpのオプションをPythonの引数として渡す
        stdout, stderr = wrapper.compare(
            old_jar=old_jar_path,
            new_jar=new_jar_path,
            html_output=output_report_path, # HTMLレポートの出力パス
            # 必要に応じて他のjapicmpオプションをここに追加 (例: access_modifier='public')
            # access_modifier='public', 
            # only_incompatible=True,
        )
        
        # japicmpの標準出力と標準エラー出力はwrapperが既にキャプチャしている
        # ここでは単に表示する
        if stdout:
            print("japicmpの標準出力:\n", stdout)
        if stderr:
            print("japicmpの標準エラー出力:\n", stderr)
        
        print(f"API差分分析が完了しました。レポート: {output_report_path}")
        return output_report_path

    # FileNotFoundErrorはJapicmpWrapperの__init__で発生する
    except FileNotFoundError as e:
        print(f"エラー: japicmp JARが見つかりません: {e}")
        return None
    # subprocess.CalledProcessErrorはJapicmpWrapperのcompareで発生し、ラッパー内で捕捉・再送出される
    except subprocess.CalledProcessError as e:
        print(f"エラー: japicmpラッパーの実行中に問題が発生しました。詳細を上記標準エラー出力で確認してください。")
        # e.stdout や e.stderr はラッパー内で表示済みの場合が多いので、ここでの再表示は控えめに
        return None
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e}")
        return None

# このファイルが直接実行された場合にのみテストコードを実行するブロック
if __name__ == "__main__":
    print("--- 005japicmp_analyzer.py を直接実行しています（テストモード） ---")
    
    # japicmp-jar-with-dependencies.jarのパス
    japicmp_tool_path = "/Users/monnotakahiro/Desktop/dev/tools/japicmp-0.23.1-jar-with-dependencies.jar" 

    # テスト用のJARファイルのパス (jar_downloader.pyでダウンロードしたものを想定)
    old_jar = "test_jars/mina-core-2.1.5.jar" 
    new_jar = "test_jars/mina-core-2.2.1.jar"

    print(f"japicmpツールパス: {japicmp_tool_path if japicmp_tool_path else '自動検出（JapicmpWrapper）'}")
    print(f"古いJARパス: {old_jar}")
    print(f"新しいJARパス: {new_jar}")

    # API差分分析を実行
    report_path = analyze_api_diff(old_jar, new_jar, japicmp_tool_path)

    if report_path:
        print(f"\nAPI差分分析テスト成功！ レポートは {report_path} に生成されました。")
        print("このHTMLファイルをWebブラウザで開いて結果を確認してください。")
    else:
        print("\nAPI差分分析テストに失敗しました。")
    print("--- テスト実行終了 ---")
import os
import json

benchmark_dir = "./BUMP/data/benchmark"  # benchmarkディレクトリのパス
target = "slf4j-api"
result_files = []

for root, _, files in os.walk(benchmark_dir):
    for file in files:
        if file.endswith(".json"):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # JSONのどこかに"slf4j-api"が含まれているか再帰的に探索
                    def contains_target(obj):
                        if isinstance(obj, dict):
                            return any(contains_target(v) for v in obj.values())
                        elif isinstance(obj, list):
                            return any(contains_target(i) for i in obj)
                        elif isinstance(obj, str):
                            return target in obj
                        return False
                    if contains_target(data):
                        result_files.append(file_path)
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

# 結果を表示
for f in result_files:
    print(f)

# ファイル名リストを保存
with open("slf4j-api_files.txt", "w", encoding="utf-8") as out:
    for f in result_files:
        out.write(f + "\n")
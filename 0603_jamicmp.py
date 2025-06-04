import subprocess
import os

japicmp_jar_path = "/path/to/japicmp-cli.jar" # JapicmpのJARファイルへのパス
old_jar = "mina-core-2.1.5.jar"
new_jar = "mina-core-2.2.1.jar"
output_html = "japicmp_report.html"

command = [
    "java", "-jar", japicmp_jar_path,
    "--old-jar", old_jar,
    "--new-jar", new_jar,
    "--html-output", output_html
]

try:
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    print("Japicmp executed successfully.")
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)
    print(f"Report generated at: {output_html}")
except subprocess.CalledProcessError as e:
    print(f"Error executing Japicmp: {e}")
    print("STDOUT:", e.stdout)
    print("STDERR:", e.stderr)
except FileNotFoundError:
    print("Error: 'java' command or Japicmp JAR not found.")
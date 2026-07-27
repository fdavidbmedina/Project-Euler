import os
import re
import subprocess
import sys
from urllib.parse import quote

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROBLEMS_DIR = os.path.join(REPO_ROOT, "Python Code")   # <-- your folder name
README_PATH = os.path.join(REPO_ROOT, "README.md")

TABLE_START = "<!-- PROBLEMS_TABLE_START -->"
TABLE_END = "<!-- PROBLEMS_TABLE_END -->"

GITHUB_REPOSITORY = os.environ.get("GITHUB_REPOSITORY", "fdavidbmedina/Project-Euler")
BRANCH = os.environ.get("GITHUB_REF_NAME", "main")
FOLDER_NAME = "Python Code"   # <-- used to build the github link path

def get_last_commit_date(filepath):
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cd", "--date=short", "--", filepath],
            cwd=REPO_ROOT, capture_output=True, text=True, check=True,
        )
        date_str = result.stdout.strip()
        if date_str:
            y, m, d = date_str.split("-")
            return f"{int(m)}/{int(d)}/{y}"
    except subprocess.CalledProcessError:
        pass
    return ""

def parse_problem_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        title_line = f.readline().strip()
        url_line = f.readline().strip()
    title = title_line.lstrip("#").strip()
    url = url_line.lstrip("#").strip()
    return title, url

def build_rows():
    rows = []
    if not os.path.isdir(PROBLEMS_DIR):
        print(f"Problems dir not found: {PROBLEMS_DIR}", file=sys.stderr)
        return rows

    for entry in os.listdir(PROBLEMS_DIR):
        if not entry.endswith(".py"):
            continue
        stem = entry[:-3]
        if not stem.isdigit():
            continue
        number = int(stem)
        filepath = os.path.join(PROBLEMS_DIR, entry)
        try:
            title, url = parse_problem_file(filepath)
        except Exception as e:
            print(f"Skipping {entry}: {e}", file=sys.stderr)
            continue

        encoded_folder = quote(FOLDER_NAME)
        encoded_file = quote(entry)
        github_link = f"https://github.com/{GITHUB_REPOSITORY}/blob/{BRANCH}/{encoded_folder}/{encoded_file}"

        date = get_last_commit_date(filepath)
        rows.append((number, title, url, github_link, date))
    rows.sort(key=lambda r: r[0])
    return rows

def build_table(rows):
    lines = ["| # | Title | Solution | Date |", "|---|-------|----------|------|"]
    for number, title, url, github_link, date in rows:
        lines.append(f"| {number} | [{title}]({url}) | [Python]({github_link}) | {date} |")
    return "\n".join(lines)

def update_readme(table_md):
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    pattern = re.compile(re.escape(TABLE_START) + r".*?" + re.escape(TABLE_END), re.DOTALL)
    replacement = f"{TABLE_START}\n{table_md}\n{TABLE_END}"
    if pattern.search(content):
        content = pattern.sub(replacement, content)
    else:
        content += f"\n{replacement}\n"
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    rows = build_rows()
    table_md = build_table(rows)
    update_readme(table_md)
    print(f"Updated README with {len(rows)} problems.")
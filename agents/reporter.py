def generate_report(repo_url, repo_data, analysis, chart_path):
    md = f"""# 🧠 GitHub Repo Analysis

## 🔗 Repo: [{repo_url}]({repo_url})

## 📝 Recent Commits:
"""
    for c in repo_data['commits']:
        md += f"- {c}\n"

    md += "\n## 🔍 Analysis:\n"
    for line in analysis:
        md += f"- {line}\n"

    # md += "\n## 📊 Charts (rendered by Streamlit)\n"


    return md
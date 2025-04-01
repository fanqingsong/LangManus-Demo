# agents/coder.py
import matplotlib.pyplot as plt
from collections import defaultdict, Counter
from datetime import datetime
import matplotlib.dates as mdates
import re
import os


def categorize_commit(message):
    message = message.lower()
    if any(kw in message for kw in ["fix", "bug"]):
        return "🐛 Bug Fixes"
    elif any(kw in message for kw in ["add", "feature", "implement"]):
        return "✨ Features"
    elif any(kw in message for kw in ["doc", "readme"]):
        return "📄 Documentation"
    elif any(kw in message for kw in ["remove", "delete"]):
        return "🔥 Removals"
    elif any(kw in message for kw in ["update", "upgrade"]):
        return "🔧 Updates"
    elif any(kw in message for kw in ["merge", "pull"]):
        return "🔀 Merges"
    else:
        return "📦 Others"


def analyze_code_activity(repo_data):
    commit_messages = repo_data['commits']
    commit_dates = repo_data.get('commit_dates', [])

    # Chart 1: Commits per day (last 30 days)
    commit_day_counts = defaultdict(int)
    for date in commit_dates:
        day = datetime.fromisoformat(date).date()
        commit_day_counts[day] += 1
    recent_days = sorted(commit_day_counts.keys())
    counts = [commit_day_counts[day] for day in recent_days]

    plt.figure(figsize=(10, 4))
    plt.plot(recent_days, counts, marker='o', linestyle='-', color='tab:blue', label='Commits per day')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    plt.gcf().autofmt_xdate()
    plt.xlabel("Date")
    plt.ylabel("Commits")
    plt.title("📈 Commits in Last 30 Days")
    plt.legend()
    path1 = "commit_chart.png"
    plt.tight_layout()
    plt.savefig(path1)
    plt.close()

    # Chart 2: Commits per category
    commit_categories = defaultdict(list)
    category_counter = Counter()
    for msg in commit_messages:
        short_msg = re.split(r'—|@', msg)[0].strip()
        category = categorize_commit(short_msg)
        commit_categories[category].append(short_msg)
        category_counter[category] += 1

    plt.figure(figsize=(8, 4))
    cats, values = zip(*category_counter.items())
    plt.bar(cats, values, color='tab:green')
    plt.ylabel("Commits")
    plt.title("🧩 Commits by Category")
    path2 = "category_chart.png"
    plt.tight_layout()
    plt.savefig(path2)
    plt.close()

    # Chart 3: Word frequency in commit messages (basic proxy for hot areas)
    word_freq = Counter()
    for msg in commit_messages:
        words = re.findall(r'\b\w{4,}\b', msg.lower())  # only words with length >= 4
        word_freq.update(words)

    most_common = word_freq.most_common(10)
    labels, freqs = zip(*most_common)
    plt.figure(figsize=(8, 4))
    plt.bar(labels, freqs, color='tab:purple')
    plt.ylabel("Frequency")
    plt.title("🔥 Most Mentioned Topics in Commits")
    path3 = "topics_chart.png"
    plt.tight_layout()
    plt.savefig(path3)
    plt.close()

    # Build markdown report
    analysis = ["## 🔍 Commit Highlights by Category"]
    for cat, msgs in commit_categories.items():
        analysis.append(f"\n### {cat}")
        for m in msgs[:3]:
            clean_msg = m.replace("\n", " ").strip()
            analysis.append(f"- {clean_msg[:100]}{'...' if len(clean_msg) > 100 else ''}")

    charts = [path1, path2, path3]
    return analysis, charts
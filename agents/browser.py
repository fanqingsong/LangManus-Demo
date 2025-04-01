import requests
import os

def scrape_github_activity(repo_url):
    token = os.getenv("GITHUB_TOKEN")  # Set via environment or .env
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    user_repo = "/".join(repo_url.split('/')[-2:])
    api_url = f"https://api.github.com/repos/{user_repo}/commits"

    res = requests.get(api_url, headers=headers)
    res.raise_for_status()
    data = res.json()

    commits = []
    commit_dates = []

    for item in data[:20]:  # optional: increase window for better activity chart
        message = item['commit']['message']
        author = item['commit']['author']['name']
        date = item['commit']['author']['date']
        sha = item['sha'][:7]

        commits.append(f"[{sha}] {message} — {author} @ {date}")
        commit_dates.append(date)  # in ISO 8601 format (perfect for parsing)

    return {
        'repo_url': repo_url,
        'commits': commits,
        'commit_dates': commit_dates
    }

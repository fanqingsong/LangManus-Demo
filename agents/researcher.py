import requests
from bs4 import BeautifulSoup

def find_trending_repo():
    url = "https://github.com/trending/python"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    repo = soup.select_one('article h2 a')['href'].strip()
    return f"https://github.com{repo}"




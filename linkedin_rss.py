import requests
from bs4 import BeautifulSoup
from datetime import datetime
import hashlib

def fetch_jobs_from_url(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    jobs = []
    for job_card in soup.find_all('a', {'class': 'base-card__full-link'}):
        title = job_card.find('h3')
        company = job_card.find('h4')
        location = job_card.find('span', {'class': 'job-search-card__location'})
        link = job_card['href']

        if not all([title, company, location]):
            continue

        jobs.append({
            'title': title.get_text(strip=True),
            'company': company.get_text(strip=True),
            'location': location.get_text(strip=True),
            'link': link
        })
    return jobs

def generate_rss(jobs):
    now = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S +0000")
    rss_items = ""
    for job in jobs:
        uid = hashlib.md5(job['link'].encode()).hexdigest()
        rss_items += f"""<item>
            <title>{job['title']} - {job['company']} ({job['location']})</title>
            <link>{job['link']}</link>
            <guid isPermaLink="false">{uid}</guid>
            <pubDate>{now}</pubDate>
        </item>"""

    rss = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
    <title>LinkedIn Job Feed</title>
    <link>https://yourusername.github.io/linkedin-rss/feed.xml</link>
    <description>RSS feed para vagas do LinkedIn</description>
    <lastBuildDate>{now}</lastBuildDate>
    {rss_items}
</channel>
</rss>"""

    with open("feed.xml", "w", encoding="utf-8") as f:
        f.write(rss)

def main():
    jobs = []
    with open("urls.txt", "r") as f:
        urls = f.readlines()
    for url in urls:
        jobs += fetch_jobs_from_url(url.strip())
    generate_rss(jobs)

if __name__ == "__main__":
    main()

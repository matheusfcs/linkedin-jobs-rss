import requests
from bs4 import BeautifulSoup
from datetime import datetime, UTC
import hashlib

def fetch_jobs_from_url(url):
    print(f"Fetching jobs from: {url}")
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    jobs = []
    job_cards = soup.find_all('a', {'class': 'base-card__full-link'})
    print(f"Found {len(job_cards)} job cards on the page.")
    for idx, job_card in enumerate(job_cards, 1):
        title = job_card.find('h3')
        company = job_card.find('h4')
        location = job_card.find('span', {'class': 'job-search-card__location'})
        link = job_card['href']

        # if not all([title, company, location]):
        #     print(f"Skipping job card {idx}: missing title, company, or location.")
        #     continue

        job_info = {
            'title': title.get_text(strip=True) if title else 'Title not found',
            'company': company.get_text(strip=True) if company else 'Company not found',
            'location': location.get_text(strip=True) if location else 'Location not found',
            'link': link
        }
        print(f"Job {idx}: {job_info['title']} at {job_info['company']} ({job_info['location']})")
        jobs.append(job_info)
    print(f"Total jobs scraped from {url}: {len(jobs)}")
    return jobs

def generate_rss(jobs):
    now = datetime.now(UTC).strftime("%a, %d %b %Y %H:%M:%S +0000")
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

    print(f"Writing {len(jobs)} jobs to feed.xml")
    with open("feed.xml", "w", encoding="utf-8") as f:
        f.write(rss)

def main():
    jobs = []
    with open("urls.txt", "r") as f:
        urls = f.readlines()
    print(f"Processing {len(urls)} URLs from urls.txt")
    for url in urls:
        jobs += fetch_jobs_from_url(url.strip())
    generate_rss(jobs)
    print("Done.")

if __name__ == "__main__":
    main()

from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/api/job_postings')
def job_postings():
    skill = request.args.get('skill')
    url = f'https://www.naukri.com/{skill}-jobs'
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    job_listings = []
    for job in soup.find_all('div', class_='jobTuple'):
        title = job.find('a', class_='title').text.strip()
        company = job.find('a', class_='subTitle').text.strip()
        location = job.find('li', class_='location').text.strip()
        link = job.find('a', class_='title')['href']
        
        job_listings.append({
            'title': title,
            'company': company,
            'location': location,
            'link': link
        })
    
    return jsonify(job_listings)

if __name__ == '__main__':
    app.run(debug=True)

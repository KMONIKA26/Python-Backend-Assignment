from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
import redis
from apscheduler.schedulers.background import BackgroundScheduler
import time

app = Flask(__name__)

# Redis setup (connect to Redis server)
redis_instance = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Function to scrape the Nifty 50 data
def scrape_nifty_50():
    url = 'https://www.nseindia.com/'
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Example: Locate the 'Nifty 50' table (this is an approximation, actual class/id may vary)
        nifty_50_table = soup.find('table', {'class': 'Nifty50-table'})
        
        # Scrape the relevant rows
        rows = nifty_50_table.find_all('tr')[1:]  # Skipping the header row

        nifty_data = []
        for row in rows:
            columns = row.find_all('td')
            stock_data = {
                'name': columns[0].text.strip(),
                'last_price': columns[1].text.strip(),
                'change': columns[2].text.strip(),
                'percentage_change': columns[3].text.strip()
            }
            nifty_data.append(stock_data)
        
        # Store data in Redis with a timestamp
        redis_instance.set('nifty_50_data', str(nifty_data))
        redis_instance.set('last_updated', time.strftime('%Y-%m-%d %H:%M:%S'))
    except Exception as e:
        print(f"Error scraping data: {e}")

# Background task to scrape data every 5 minutes
scheduler = BackgroundScheduler()
scheduler.add_job(scrape_nifty_50, 'interval', minutes=5)
scheduler.start()

# Display the data in card layout
@app.route('/')
def index():
    nifty_data = eval(redis_instance.get('nifty_50_data'))
    last_updated = redis_instance.get('last_updated')
    return render_template('index.html', nifty_data=nifty_data, last_updated=last_updated)

if __name__ == '__main__':
    scrape_nifty_50()  # Run it once at startup
    app.run(debug=True)

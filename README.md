# Python Backend Developer Assignment

This repository contains solutions to three tasks for a Python backend developer assignment. Each task is implemented as a stand-alone web application using Python frameworks and libraries such as Flask and Redis.

## Table of Contents

1. [Task 1: URL Shortener](#task-1-url-shortener)
2. [Task 2: PasteLockly](#task-2-pastelockly)
3. [Task 3: Nifty 50 Web Scraper](#task-3-nifty-50-web-scraper)
4. [Technologies Used](#technologies-used)
5. [Setup Instructions](#setup-instructions)
6. [File Structure](#file-structure)
7. [Future Enhancements](#future-enhancements)
8. [License](#license)

---

## Task 1: URL Shortener

This task implements a URL shortener web app. Users can submit a long URL through a form, and the app generates a short URL for it. When the short URL is accessed, the user is redirected to the original URL.

### Features

1. **Create Short URLs**: Users can submit long URLs and receive a short URL in return.
2. **Redirection**: Accessing the short URL redirects users to the original URL.
3. **Edge Case Handling**: Includes handling of invalid URLs and duplicate entries.
4. **Optimizations**: Efficient space and time management for storing and retrieving URLs.

---

## Task 2: PasteLockly

PasteLockly is a web app that allows users to share text snippets anonymously by creating a shareable URL. Users can also encrypt their snippets with a secret key, which will be required for viewing the content.

### Features

1. **Shareable Text Snippets**: Users can post text snippets and generate a shareable URL.
2. **View-Only Snippets**: The generated URL allows only view access to the snippet.
3. **Optional Encryption**: Users can add a secret key to encrypt the snippet, which will need to be provided to view it.
4. **Secure Viewing**: The viewer must supply the correct secret key to decrypt and view the snippet.

---

## Task 3: Nifty 50 Web Scraper

This task implements a web app that scrapes stock market data (Nifty 50) from [NSE India](https://www.nseindia.com/) every 5 minutes. The scraped data is stored in Redis and displayed in a card layout.

### Features

1. **Scrape Nifty 50 Data**: Scrapes the Nifty 50 stock data from the NSE India website every 5 minutes.
2. **Redis Storage**: Persists the scraped data in Redis for fast and efficient retrieval.
3. **Card Layout**: Displays the scraped stock data in a visually appealing card format.
4. **Background Scheduling**: A background task automatically scrapes the data at 5-minute intervals.

---

## Technologies Used

- **Flask**: Lightweight Python web framework for building the backend of all three tasks.
- **Redis**: In-memory data structure store used in Task 3 for caching the scraped data.
- **BeautifulSoup**: Used for parsing HTML content from the NSE India website in Task 3.
- **Requests**: For making HTTP requests in the Nifty 50 web scraper.
- **APScheduler**: Schedules the background task to scrape data every 5 minutes in Task 3.
- **HTML5 + CSS3**: Used to build user-friendly interfaces for each task.
- **SQLite (or similar)**: Can be used for URL and text storage in Task 1 and Task 2.

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/python-backend-assignment.git
cd python-backend-assignment
```

### 2. Install Dependencies

Install the necessary Python packages for all tasks:
```bash
pip install Flask requests beautifulsoup4 redis apscheduler
```

### 3. Start Redis

Ensure Redis is installed and running for Task 3:
```bash
# For Ubuntu:
sudo apt-get install redis-server
redis-server
```

### 4. Run Each Task

You can run each task individually as a Flask app.

#### To Run Task 1: URL Shortener
```bash
cd url_shortener
python app.py
```
Access the app in your browser at `http://127.0.0.1:5000`.

#### To Run Task 2: PasteLockly
```bash
cd pastelockly
python app.py
```
Access the app in your browser at `http://127.0.0.1:5000`.

#### To Run Task 3: Nifty 50 Web Scraper
```bash
cd nifty_scraper
python web_scraper.py
```
Access the app in your browser at `http://127.0.0.1:5000`.

---

## Future Enhancements

### Task 1: URL Shortener
- **Analytics**: Add tracking for how many times each shortened URL is accessed.
- **Expiration**: Add expiration dates for shortened URLs.

### Task 2: PasteLockly
- **Expiration**: Allow users to set expiration times for the snippets.
- **Snippet Versioning**: Add version control to view older versions of a snippet.

### Task 3: Nifty 50 Web Scraper
- **Data Visualization**: Add charts or graphs to better represent stock trends.
- **Search and Filter**: Allow users to filter and search for specific stocks.
- **Responsive Design**: Improve mobile responsiveness for the card layout.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

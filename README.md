# 🕵️‍♂️ ScrapeIT

**ScrapeIT** is a Python + Flask based **web scraping and price comparison tool** that helps users compare product prices across **Amazon**, **Flipkart**, and **JioMart** — all in one place.

---

## 📘 Table of Contents

1. [Overview](#-overview)  
2. [Features](#-features)  
3. [Tech Stack](#-tech-stack)  
4. [Project Structure](#-project-structure)  
5. [Installation](#-installation)  
6. [Usage](#-usage)  
7. [How It Works](#-how-it-works)  
8. [Screenshots](#-screenshots)  
9. [Known Issues](#-known-issues)  
10. [Future Improvements](#-future-improvements)  
11. [Author](#-author)  
12. [License](#-license)

---

## 🔍 Overview

**ScrapeIT** (also known as *PersonalProject2019*) is a lightweight Flask application that allows users to search for any product and instantly view the **product name**, **price**, and **image link** from the top three Indian e-commerce websites — **Amazon**, **Flipkart**, and **JioMart**.

It automates the tedious process of switching between sites, making online shopping faster and smarter.

---

## ✨ Features

✅ Search any product name once — get results from **three major platforms**  
✅ Displays product **titles**, **prices**, and **images** in a clean layout  
✅ Built with **Flask** and **BeautifulSoup4**  
✅ Simple and responsive frontend (HTML/CSS)  
✅ Fully local — no database or API required  
✅ Modular scraping functions for easy extension  

---

## 🧰 Tech Stack

| Layer | Technology |
|-------|-------------|
| **Backend** | Python, Flask |
| **Scraping** | Requests, BeautifulSoup4 |
| **Frontend** | HTML, CSS |
| **Libraries Used** | `flask`, `requests`, `beautifulsoup4`, `tabulate`, `selenium` (optional) |
| **Platform Support** | Amazon India, Flipkart, JioMart |

---

## 📂 Project Structure

```
ScrapeIT/
├── main.py                # Flask app entry point
├── password.py            # Local credential file (if used)
├── templates/
│   ├── index.html         # Homepage (search input)
│   └── result.html        # Comparison results page
├── static/
│   ├── style.css          # Styling for pages
│   └── ...                # Other static assets
├── git_images/            # Screenshots for README
├── requirements.txt       # Python dependencies
└── README.md              # Documentation (this file)
```

---

## ⚙️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/gupta-ritik/ScrapeIT.git
cd ScrapeIT
```

### 2. Create a Virtual Environment (Recommended)
```bash
python -m venv venv
# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

> If `requirements.txt` is missing, install manually:
```bash
pip install flask requests beautifulsoup4 tabulate selenium
```

### 4. Run the Application
```bash
python main.py
```

### 5. Open in Browser
Visit: [http://127.0.0.1:5000](http://127.0.0.1:5000)

You’ll see the search interface where you can type a product name.

---

## 🧠 How It Works

1. **User Input:**  
   The user enters a search query (e.g., “iPhone 14 Pro”) on the home page.

2. **Scraping Process:**  
   - Flask receives the request.  
   - For each website (Amazon, Flipkart, JioMart), a separate scraping function runs.  
   - These functions:
     - Construct the search URL
     - Fetch the HTML page via `requests`
     - Parse it using `BeautifulSoup`
     - Extract product names, prices, and image URLs

3. **Data Aggregation:**  
   The results from all platforms are combined into a Python dictionary/list.

4. **Display:**  
   Flask passes this data to `result.html`, which renders it in a neatly formatted table or card layout.

5. **Result:**  
   You get a quick **side-by-side price comparison** across three e-commerce sites.

---

## 🖼️ Screenshots

### 🏠 Home Page
![Home Page](git_images/homepage.png)

### 📊 Comparison Results
![Result Page](git_images/resultpage.png)

*(If the screenshots have different filenames, update the links above accordingly.)*

---

## ⚠️ Known Issues

- Websites may change their **HTML structure**, which can break the scraping logic.  
- Some items might not appear due to **dynamic JS loading** or **CAPTCHA blocks**.  
- Amazon / Flipkart may temporarily block frequent scraping requests.  
- No data persistence — each search is re-scraped every time.  

---

## 🚀 Future Improvements

- ✅ Add database (SQLite / MongoDB) to cache recent searches  
- ✅ Add more e-commerce sites (e.g., Myntra, eBay)  
- ✅ Add asynchronous scraping for faster performance  
- ✅ Integrate Selenium / Playwright for JS-rendered pages  
- ✅ Add price-trend tracking over time  
- ✅ Add user login to save favorite searches  
- ✅ Add API endpoint for external integration  

---

## 👨‍💻 Author

**Ritik Gupta**  
📧 [ritikgupta1807@gmail.com](mailto:ritiknitc@gmail.com)  
🔗 [GitHub Profile](https://github.com/gupta-ritik)  

---

## 📜 License

This project is open-source under the **MIT License** — feel free to use, modify, and distribute it as long as proper credit is given.

---

## ⭐ Support

If you like this project:
- 🌟 Star this repository  
- 🍴 Fork it to make your own improvements  
- 🐛 Submit an issue or PR if you find bugs  

---

> _“Scrape smart, shop smarter — with ScrapeIT.”_

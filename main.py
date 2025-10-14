from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as Options_Chrome

# Initialize lists
search_queries = []

jiomart_names = []
jiomart_prices = []
jiomart_imagelinks = []
jiomart_prices_clean = []
jiomart_ratings = []

flipkart_names = []
flipkart_prices = []
flipkart_prices_clean = []
flipkart_imagelinks = []
flipkart_ratings = []

amazon_names = []
amazon_prices = []
amazon_prices_clean = []
amazon_imagelinks = []
amazon_ratings = []


def clear_all_lists():
    """Clear all global lists"""
    search_queries.clear()
    
    jiomart_names.clear()
    jiomart_prices.clear()
    jiomart_prices_clean.clear()
    jiomart_imagelinks.clear()
    jiomart_ratings.clear()
    
    flipkart_names.clear()
    flipkart_prices.clear()
    flipkart_prices_clean.clear()
    flipkart_imagelinks.clear()
    flipkart_ratings.clear()
    
    amazon_names.clear()
    amazon_prices.clear()
    amazon_prices_clean.clear()
    amazon_imagelinks.clear()
    amazon_ratings.clear()


# Clear lists on startup
clear_all_lists()

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form.get('u', '')
    processed_text = text.lower().strip()
    
    if not processed_text:
        return render_template("index.html", error="Please enter a search term")
    
    search_queries.append(processed_text)
    product_search = search_queries[0]
    
    try:
        # Scrape all websites
        print(f"Scraping for: {product_search}")
        scrape_amazon(product_search)
        scrape_flipkart(product_search)
        scrape_jiomart(product_search)
        
        # Process and clean data
        process_data()
        
        # Prepare data for display
        flipkart_data = prepare_data(flipkart_names, flipkart_prices_clean, flipkart_imagelinks, flipkart_ratings)
        amazon_data = prepare_data(amazon_names, amazon_prices_clean, amazon_imagelinks, amazon_ratings)
        jiomart_data = prepare_data(jiomart_names, jiomart_prices_clean, jiomart_imagelinks, jiomart_ratings)
        
        print(f"Found {len(amazon_data)} Amazon products")
        print(f"Found {len(flipkart_data)} Flipkart products")
        print(f"Found {len(jiomart_data)} JioMart products")
        
        # Clear lists for next search
        clear_all_lists()
        
        return render_template(
            "result.html",
            flipkart=flipkart_data,
            amazon=amazon_data,
            jiomart=jiomart_data
        )
        
    except Exception as e:
        print(f"Error during scraping: {e}")
        clear_all_lists()
        return render_template("index.html", error="An error occurred. Please try again.")


def prepare_data(names, prices, images, ratings):
    """Prepare data as tuples for template rendering"""
    min_length = min(len(names), len(prices), len(images), len(ratings))
    return [(names[i], prices[i], images[i], ratings[i]) for i in range(min_length)]


def scrape_amazon(product_search):
    """Scrape Amazon for products"""
    print("Scraping Amazon...")
    
    URL = f"https://www.amazon.in/s?k={product_search.replace(' ', '+')}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0',
        'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    
    try:
        print("Using Selenium for Amazon (better success rate)...")
        options = Options_Chrome()
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument(f'user-agent={headers["User-Agent"]}')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        browser = webdriver.Chrome(options=options)
        browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        browser.get(URL)
        time.sleep(5)
        
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        browser.quit()
        
        products = soup.find_all("div", {"data-component-type": "s-search-result"})
        
        if not products:
            products = soup.find_all("div", {"class": "s-result-item"})
        
        print(f"Found {len(products)} product containers")
        
        for product in products[:20]:
            if product.get('data-component-type') == 's-sponsored-result':
                continue
            
            name = None
            name_selectors = [
                ("h2", {"class": "a-size-mini"}),
                ("span", {"class": "a-size-medium"}),
                ("span", {"class": "a-size-base-plus"}),
                ("h2", "a-size-base-plus"),
                ("h2", None),
            ]
            
            for tag, class_name in name_selectors:
                if class_name:
                    name_elem = product.find(tag, {"class": class_name})
                else:
                    name_elem = product.find(tag)
                    
                if name_elem:
                    name = name_elem.get_text(strip=True)
                    if name and len(name) > 10:
                        break
            
            if name:
                amazon_names.append(name)
            else:
                continue
            
            price = "N/A"
            price_elem = product.find("span", {"class": "a-price-whole"})
            if price_elem:
                price = price_elem.get_text(strip=True)
            amazon_prices.append(price)
            
            rating = "N/A"
            rating_elem = product.find("span", {"class": "a-icon-alt"})
            if rating_elem:
                rating_text = rating_elem.get_text(strip=True)
                if "out of" in rating_text:
                    rating = rating_text.split()[0]
            amazon_ratings.append(rating)
            
            img_elem = product.find("img", {"class": "s-image"})
            if img_elem and 'src' in img_elem.attrs:
                amazon_imagelinks.append(img_elem['src'])
            else:
                amazon_imagelinks.append("https://via.placeholder.com/200x200?text=No+Image")
        
        print(f"Amazon: Found {len(amazon_names)} products")
                
    except Exception as e:
        print(f"Amazon scraping error: {e}")
        import traceback
        traceback.print_exc()


def scrape_jiomart(product_search):
    """Scrape JioMart for products"""
    print("Scraping JioMart...")
    
    try:
        URL = f"https://www.jiomart.com/search/{product_search.replace(' ', '%20')}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }
        
        # JioMart requires JavaScript, so we'll use Selenium
        print("Using Selenium for JioMart...")
        options = Options_Chrome()
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--window-size=1920,1080')
        options.add_argument(f'user-agent={headers["User-Agent"]}')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        browser = webdriver.Chrome(options=options)
        browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        browser.get(URL)
        time.sleep(8)  # Wait for content to load
        
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        browser.quit()
        
        # Find product containers - JioMart structure
        products = soup.find_all("div", {"class": "plp-card-container"}) or \
                  soup.find_all("div", {"class": "ais-Hits-item"}) or \
                  soup.find_all("a", {"class": "plp-card-wrapper"})
        
        print(f"Found {len(products)} JioMart product containers")
        
        for product in products[:20]:
            # Scrape name
            name_elem = (
                product.find("div", {"class": "plp-card-details-name"}) or
                product.find("h3") or
                product.find("span", {"class": "jm-body-xs"})
            )
            
            if name_elem:
                name = name_elem.get_text(strip=True)
                jiomart_names.append(name if name else "Product Name Not Available")
            else:
                jiomart_names.append("Product Name Not Available")
            
            # Scrape price
            price_elem = (
                product.find("span", {"class": "jm-heading-xxs"}) or
                product.find("span", {"id": "final_price"}) or
                product.find("div", {"class": "plp-card-details-price"})
            )
            
            if price_elem:
                price = price_elem.get_text(strip=True)
                jiomart_prices.append(price)
            else:
                jiomart_prices.append("N/A")
            
            # JioMart doesn't typically show ratings on listing pages
            jiomart_ratings.append("N/A")
            
            # Scrape image
            img_elem = product.find("img")
            if img_elem:
                image_src = img_elem.get('src') or img_elem.get('data-src')
                if image_src:
                    jiomart_imagelinks.append(image_src)
                else:
                    jiomart_imagelinks.append("https://via.placeholder.com/200x200?text=No+Image")
            else:
                jiomart_imagelinks.append("https://via.placeholder.com/200x200?text=No+Image")
        
        print(f"JioMart: Found {len(jiomart_names)} names, {len(jiomart_prices)} prices, {len(jiomart_imagelinks)} images")
                    
    except Exception as e:
        print(f"JioMart scraping error: {e}")
        import traceback
        traceback.print_exc()


def scrape_flipkart(product_search):
    """Scrape Flipkart for products"""
    print("Scraping Flipkart...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
    }
    
    URL = f"https://www.flipkart.com/search?q={product_search}"
    
    try:
        session = requests.Session()
        response = session.get(URL, headers=headers, timeout=15)
        response.raise_for_status()
        html_content = response.text
        
    except Exception as e:
        print(f"Flipkart direct scraping failed: {e}")
        try:
            print("Using Selenium fallback for Flipkart...")
            options = Options_Chrome()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            browser = webdriver.Chrome(options=options)
            browser.get(URL)
            time.sleep(8)
            html_content = browser.page_source
            browser.quit()
        except Exception as e:
            print(f"Flipkart scraping error (Selenium): {e}")
            return
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    product_containers = (
        soup.find_all("div", {"class": "_1AtVbE"}) or
        soup.find_all("div", {"class": "_13oc-S"}) or
        soup.find_all("div", {"class": "tUxRFH"}) or
        soup.find_all("div", {"class": "_1sdMkc"}) or
        soup.find_all("a", {"class": "CGtC98"})
    )
    
    for container in product_containers[:20]:
        name = None
        name_elem = (
            container.find("div", {"class": "_4rR01T"}) or
            container.find("a", {"class": "IRpwTa"}) or
            container.find("a", {"class": "s1Q9rs"}) or
            container.find("div", {"class": "KzDlHZ"}) or
            container.find("div", {"class": "_2WkVRV"})
        )
        
        if name_elem:
            name = name_elem.get_text(strip=True)
            flipkart_names.append(name if name else "Product Name Not Available")
        else:
            flipkart_names.append("Product Name Not Available")
        
        price_elem = (
            container.find("div", {"class": "_30jeq3"}) or
            container.find("div", {"class": "Nx9bqj"}) or
            container.find("div", {"class": "_1_WHN1"}) or
            container.find("div", {"class": "_25b18c"})
        )
        
        if price_elem:
            price = price_elem.get_text(strip=True)
            flipkart_prices.append(price)
        else:
            flipkart_prices.append("N/A")
        
        rating = "N/A"
        rating_elem = (
            container.find("div", {"class": "_3LWZlK"}) or
            container.find("div", {"class": "XQDdHH"}) or
            container.find("span", {"class": "_1lRcqv"})
        )
        
        if rating_elem:
            rating_text = rating_elem.get_text(strip=True)
            rating = ''.join(c for c in rating_text if c.isdigit() or c == '.')
            if rating:
                flipkart_ratings.append(rating)
            else:
                flipkart_ratings.append("N/A")
        else:
            flipkart_ratings.append("N/A")
        
        img_elem = container.find("img")
        if img_elem and 'src' in img_elem.attrs:
            flipkart_imagelinks.append(img_elem['src'])
        else:
            flipkart_imagelinks.append("https://via.placeholder.com/200x200?text=No+Image")
    
    print(f"Flipkart: Found {len(flipkart_names)} names, {len(flipkart_prices)} prices, {len(flipkart_ratings)} ratings, {len(flipkart_imagelinks)} images")


def process_data():
    """Clean and process scraped data"""
    # Clean JioMart prices
    for price in jiomart_prices:
        cleaned = price.strip().replace("₹", "").replace("Rs.", "").replace("Rs", "").replace(",", "").strip()
        if cleaned:
            jiomart_prices_clean.append(cleaned)
    
    # Clean Flipkart prices
    for price in flipkart_prices:
        cleaned = price.strip().replace("₹", "").replace(",", "").strip()
        if cleaned:
            flipkart_prices_clean.append(cleaned)
    
    # Clean Amazon prices
    for price in amazon_prices:
        cleaned = price.replace(",", "").replace(".", "").strip()
        if cleaned:
            amazon_prices_clean.append(cleaned)


if __name__ == "__main__":
    app.run(debug=True)
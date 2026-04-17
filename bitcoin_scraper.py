import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

class BitcoinScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def scrape_coinmarketcap(self):
        """Scrape Bitcoin price from CoinMarketCap"""
        try:
            url = 'https://coinmarketcap.com/currencies/bitcoin/'
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            price_element = soup.find('span', {'data-test': 'text-cdp-price-price'})
            if price_element:
                price = price_element.text
                return {
                    'source': 'CoinMarketCap',
                    'price': price,
                    'timestamp': datetime.now().isoformat()
                }
        except Exception as e:
            print(f"Error scraping CoinMarketCap: {e}")
        return None
    
    def scrape_coingecko(self):
        """Scrape Bitcoin price from CoinGecko API"""
        try:
            url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd'
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if 'bitcoin' in data:
                price = data['bitcoin']['usd']
                return {
                    'source': 'CoinGecko',
                    'price': f'${price:,.2f}',
                    'timestamp': datetime.now().isoformat()
                }
        except Exception as e:
            print(f"Error scraping CoinGecko: {e}")
        return None
    
    def get_all_prices(self):
        """Get Bitcoin prices from multiple sources"""
        results = []
        results.append(self.scrape_coingecko())
        results.append(self.scrape_coinmarketcap())
        return [r for r in results if r is not None]

if __name__ == '__main__':
    scraper = BitcoinScraper()
    prices = scraper.get_all_prices()
    
    print('=== Bitcoin Price Information ===')
    for price_data in prices:
        print(f"\nSource: {price_data['source']}")
        print(f"Price: {price_data['price']}")
        print(f"Time: {price_data['timestamp']}")
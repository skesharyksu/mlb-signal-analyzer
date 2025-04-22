import requests
from bs4 import BeautifulSoup
import json
import logging
from typing import Dict, List, Optional
import time
from pathlib import Path
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class WebScraper:
    def __init__(self, base_url: str):
        """
        Initialize the WebScraper with a base URL.
        
        Args:
            base_url (str): The base URL of the website to scrape
        """
        self.base_url = base_url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
        
    def get_page(self, url: str) -> Optional[BeautifulSoup]:
        """
        Fetch a webpage and return its BeautifulSoup object.
        
        Args:
            url (str): The URL to fetch
            
        Returns:
            Optional[BeautifulSoup]: The parsed HTML content or None if the request failed
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'lxml')
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            return None
            
    def save_data(self, data: List[Dict], filename: str) -> bool:
        """
        Save scraped data to a JSON file.
        
        Args:
            data (List[Dict]): The data to save
            filename (str): The name of the output file
            
        Returns:
            bool: True if the save was successful, False otherwise
        """
        try:
            # Create data directory if it doesn't exist
            data_dir = Path('data')
            data_dir.mkdir(exist_ok=True)
            
            # Save the data
            output_path = data_dir / filename
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Data saved to {output_path}")
            return True
        except Exception as e:
            logger.error(f"Error saving data: {str(e)}")
            return False
            
    def scrape(self) -> List[Dict]:
        """
        Main scraping method to be implemented by subclasses.
        
        Returns:
            List[Dict]: The scraped data
        """
        raise NotImplementedError("Subclasses must implement this method")
        
    def run(self, output_file: str = 'scraped_data.json') -> bool:
        """
        Run the scraper and save the results.
        
        Args:
            output_file (str): The name of the output file
            
        Returns:
            bool: True if the scraping and saving were successful, False otherwise
        """
        try:
            logger.info(f"Starting scrape of {self.base_url}")
            data = self.scrape()
            if data:
                return self.save_data(data, output_file)
            return False
        except Exception as e:
            logger.error(f"Error during scraping: {str(e)}")
            return False

if __name__ == "__main__":
    # Example usage
    class ExampleScraper(WebScraper):
        def scrape(self) -> List[Dict]:
            soup = self.get_page(self.base_url)
            if not soup:
                return []
                
            # Implement your scraping logic here
            data = []
            # ... scraping code ...
            
            return data
            
    # Create and run the scraper
    scraper = ExampleScraper("https://example.com")
    scraper.run() 
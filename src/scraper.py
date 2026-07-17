"""
Web scraper for extracting Mikew's performance schedule from NAC Busking website
"""
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NACBuskingScraper:
    def __init__(self, busker_id):
        self.busker_id = busker_id
        self.base_url = "https://eservices.nac.gov.sg/Busking/busker/profile/"
        self.session = requests.Session()
        
    def get_busker_profile(self):
        """
        Fetch the busker's profile page
        """
        url = f"{self.base_url}{self.busker_id}"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.error(f"Error fetching profile: {e}")
            return None
            
    def parse_performance_schedule(self, html_content):
        """
        Parse the HTML content to extract performance schedule information
        """
        if not html_content:
            return []
            
        soup = BeautifulSoup(html_content, 'html.parser')
        performances = []
        
        # Look for schedule information in the page
        # Since we couldn't see the schedule in our initial inspection,
        # we'll need to look for common patterns
        
        # Look for tables or divs that might contain schedule data
        schedule_elements = soup.find_all(['table', 'div'], class_=re.compile(r'schedule|event|performance', re.I))
        
        # Also look for date/time patterns
        date_time_pattern = r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b\d{1,2}:\d{2}\s*(?:AM|PM|am|pm)?\b'
        
        # Extract text and search for dates/times
        page_text = soup.get_text()
        potential_dates = re.findall(date_time_pattern, page_text)
        
        # Look for location information
        location_keywords = ['location', 'venue', 'place', 'area']
        location_elements = []
        for keyword in location_keywords:
            elements = soup.find_all(text=re.compile(keyword, re.I))
            location_elements.extend(elements)
            
        # For now, we'll return what we can find
        # In a real implementation, we'd need to refine this based on actual page structure
        return {
            'busker_name': self.extract_busker_name(soup),
            'performances': [],  # Will be populated with actual performance data
            'scraped_at': datetime.now().isoformat(),
            'potential_dates': potential_dates,
            'location_elements': [str(el)[:100] for el in location_elements[:5]]  # First 5 location elements
        }
        
    def extract_busker_name(self, soup):
        """
        Extract the busker's name from the profile page
        """
        # Look for h1, h2, or elements with class containing 'name'
        name_element = soup.find('h2') or soup.find('h1') or soup.find(class_=re.compile(r'name', re.I))
        if name_element:
            return name_element.get_text(strip=True)
        return "Unknown Busker"
        
    def run_scraper(self):
        """
        Main method to run the scraper
        """
        logger.info("Starting scraper for busker ID: %s", self.busker_id)
        
        # Get the profile page
        html_content = self.get_busker_profile()
        
        if not html_content:
            logger.error("Failed to retrieve profile page")
            return None
            
        # Parse the schedule information
        schedule_data = self.parse_performance_schedule(html_content)
        
        logger.info("Scraping completed successfully")
        return schedule_data

# Example usage
if __name__ == "__main__":
    # Mikew's busker ID from the URL
    BUSKER_ID = "dbc5b6bc-e22a-4e60-9fe4-f4d6a1aa17a4"
    
    scraper = NACBuskingScraper(BUSKER_ID)
    schedule = scraper.run_scraper()
    
    if schedule:
        print("Busker:", schedule['busker_name'])
        print("Scraped at:", schedule['scraped_at'])
        print("Potential dates found:", schedule['potential_dates'])
        print("Location elements:", schedule['location_elements'])
    else:
        print("Failed to scrape schedule")
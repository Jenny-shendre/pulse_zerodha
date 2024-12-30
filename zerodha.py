import requests
from bs4 import BeautifulSoup
import csv

def scrape_zerodha_pulse():
    # URL of the Zerodha Pulse website
    url = "https://pulse.zerodha.com"
    
    try:
        # Send a GET request to the website
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Create a list to store the scraped data
        scraped_data = []
        
        # Find all main list items containing articles
        articles = soup.find_all('li', class_='box item')  # Adjust selector based on the structure
        
        if not articles:
            print("No articles found. Verify the HTML structure or update selectors.")
            return
        
        for idx, article in enumerate(articles, start=1):  # Add serial numbers starting from 1
            # Extract title
            title_tag = article.find('h2', class_='title')
            title = title_tag.get_text(strip=True) if title_tag else 'N/A'
            
            # Extract summary
            desc_tag = article.find('div', class_='desc')
            desc = desc_tag.get_text(strip=True) if desc_tag else 'N/A'
            
            # Extract time
            date_tag = article.find('span', class_='date')
            date = date_tag.get_text(strip=True) if date_tag else 'N/A'
            
            # Extract source
            feed_tag = article.find('span', class_='feed')
            feed = feed_tag.get_text(strip=True) if feed_tag else 'N/A'
            
            # Print the data to the console
            print(f"{idx}. Title: {title}")
            print(f"   Summary: {desc}")
            print(f"   Time: {date}")
            print(f"   Source: {feed}")
            print("-" * 50)
            
            # Append the data to the list
            scraped_data.append([idx, title, desc, date, feed])
        
        # Save the necessary data to a CSV file
        file_name = "pulse_zerodha_data.csv"
        
        with open(file_name, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['S.No', 'Heading', 'Summary', 'Time', 'Source'])  # Column headers
            writer.writerows(scraped_data)
        
        print(f"Data successfully scraped and saved to '{file_name}'.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Run the scraper
scrape_zerodha_pulse()

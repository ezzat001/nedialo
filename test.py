import requests
from bs4 import BeautifulSoup
import time

# Define the base URL for Yellow Pages search (you can modify the search query and location)
BASE_URL = 'https://www.yellowpages.com.lb/search?query={query}&location={location}'

# Define a function to fetch and parse the page
def get_yellow_pages_results(query, location):
    # Format the search URL
    url = BASE_URL.format(query=query, location=location)
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code != 200:
        print(f"Error fetching page {url}, status code: {response.status_code}")
        return None

    # Parse the page using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

# Define a function to extract business details from the results page
def extract_business_details(soup):
    business_details = []
    
    # Find the container that holds business listing information
    listings = soup.find_all('div', class_='listing-info')

    # Loop through each listing and extract the business info
    for listing in listings:
        name = listing.find('h2').text.strip() if listing.find('h2') else 'N/A'
        phone = listing.find('div', class_='phone-number').text.strip() if listing.find('div', class_='phone-number') else 'N/A'
        address = listing.find('div', class_='address').text.strip() if listing.find('div', class_='address') else 'N/A'
        
        business_details.append({
            'name': name,
            'phone': phone,
            'address': address
        })
    
    return business_details

# Define the main function to fetch and display the details
def fetch_roofing_companies(query, location):
    # Get the Yellow Pages results page
    soup = get_yellow_pages_results(query, location)
    
    if soup:
        # Extract business details
        businesses = extract_business_details(soup)
        
        # Print the extracted details
        for business in businesses:
            print(f"Name: {business['name']}")
            print(f"Phone: {business['phone']}")
            print(f"Address: {business['address']}")
            print("-" * 50)

# Example usage: Fetch roofing companies in a specified location
if __name__ == '__main__':
    query = 'roofing'  # Search term
    location = 'New York'  # Location (modify as needed)
    
    fetch_roofing_companies(query, location)

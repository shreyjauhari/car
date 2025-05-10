import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import time
import random
import os

def scrape_olx_car_covers(max_pages=5):
    """
    Scrape car cover listings from OLX India and save to CSV
    
    Args:
        max_pages: Maximum number of pages to scrape
    """
    base_url = "https://www.olx.in/items/q-car-cover"
    
    # Create a list to store all results
    all_results = []
    
    # Set headers to mimic a browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Referer': 'https://www.olx.in/',
        'Connection': 'keep-alive',
    }
    
    # Loop through pages
    for page_num in range(1, max_pages + 1):
        try:
            # Construct page URL (first page is just base_url)
            if page_num == 1:
                page_url = base_url
            else:
                page_url = f"{base_url}?page={page_num}"
                
            print(f"Scraping page {page_num}: {page_url}")
            
            # Send GET request to the page
            response = requests.get(page_url, headers=headers)
            
            # Check if request was successful
            if response.status_code == 200:
                # Parse HTML content
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find all listings on the page
                # Note: The actual class names and structure may change, so we need to inspect the site
                listings = soup.select('li.EIR5N')
                
                if not listings:
                    print(f"No listings found on page {page_num}. The page structure might have changed.")
                    break
                
                # Process each listing
                for listing in listings:
                    try:
                        # Extract relevant information
                        title_elem = listing.select_one('span.fTZT3')
                        price_elem = listing.select_one('span._2Ks63')
                        location_elem = listing.select_one('span._1KOFM')
                        date_elem = listing.select_one('span._2DGqt')
                        url_elem = listing.select_one('a')
                        
                        # Get the data, handling potential None values
                        title = title_elem.text.strip() if title_elem else "N/A"
                        price = price_elem.text.strip() if price_elem else "N/A"
                        location = location_elem.text.strip() if location_elem else "N/A"
                        date_posted = date_elem.text.strip() if date_elem else "N/A"
                        url = "https://www.olx.in" + url_elem['href'] if url_elem and 'href' in url_elem.attrs else "N/A"
                        
                        # Add to results list
                        all_results.append({
                            'Title': title,
                            'Price': price,
                            'Location': location,
                            'Date Posted': date_posted,
                            'URL': url
                        })
                        
                    except Exception as e:
                        print(f"Error processing a listing: {e}")
                        continue
                
                # Add a random delay to avoid being blocked
                time.sleep(random.uniform(1.0, 3.0))
                
            else:
                print(f"Failed to fetch page {page_num}. Status code: {response.status_code}")
                break
                
        except Exception as e:
            print(f"Error scraping page {page_num}: {e}")
            break
            
    return all_results

def save_to_csv(results, filename=None):
    """
    Save scraped results to a CSV file
    
    Args:
        results: List of dictionaries containing scraped data
        filename: Optional filename for the CSV
    
    Returns:
        The path to the saved CSV file
    """
    if not filename:
        # Create a filename with current timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"olx_car_covers_{timestamp}.csv"
    
    # Define field names for CSV
    fieldnames = ['Title', 'Price', 'Location', 'Date Posted', 'URL']
    
    # Write results to CSV
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
            
        print(f"Results saved to {filename}")
        return filename
    
    except Exception as e:
        print(f"Error saving to CSV: {e}")
        return None

def main():
    print("Starting OLX Car Cover Scraper...")
    
    # Create directory for results if it doesn't exist
    os.makedirs('olx_results', exist_ok=True)
    
    # Scrape results
    results = scrape_olx_car_covers(max_pages=3)
    
    if results:
        print(f"Scraped {len(results)} car cover listings.")
        
        # Save results to CSV in the results directory
        csv_path = os.path.join('olx_results', f"olx_car_covers_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
        saved_path = save_to_csv(results, csv_path)
        
        if saved_path:
            print(f"Results successfully saved to {saved_path}")
            print("To upload to GitHub:")
            print("1. Create a GitHub repository")
            print("2. Clone it to your local machine")
            print("3. Copy this script and the results folder into the repository directory")
            print("4. Commit and push the changes")
    else:
        print("No results found or scraping failed.")

if __name__ == "__main__":
    main()

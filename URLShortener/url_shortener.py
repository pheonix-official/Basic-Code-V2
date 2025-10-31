import pyshorteners
import sys

def shorten_url(long_url):
    """
    this shortens a given URL using the TinyURL service.
    """
    try:
        # initialise the TinyURL shortener
        s = pyshorteners.Shortener()
        
        # uses the 'tinyurl' shortener method
        short_url = s.tinyurl.short(long_url)
        
        print(f"\n Successfully shortened URL:")
        print(f"Original: {long_url}")
        print(f"Shortened: {short_url}\n")
        
    except Exception as e:
        print(f"\n An error occurred during URL shortening: {e}")
        print("Please check if the URL is valid and you have an internet connection.")

if __name__ == "__main__":
    print(" Python URL Shortener Tool ")
    
    # checks if pyshorteners is installed
    try:
        pass 
    except ImportError:
        print("\nFATAL ERROR: 'pyshorteners' library is not installed.")
        print("Please run: pip install pyshorteners\n")
        sys.exit(1)
        
    # gets the input from user
    url_to_shorten = input("Enter the long URL you want to shorten: ").strip()
    
    if url_to_shorten:
        # a simple validation to ensure it looks like a URL
        if not (url_to_shorten.startswith('http://') or url_to_shorten.startswith('https://')):
            url_to_shorten = 'https://' + url_to_shorten
            print(f"Prepending 'https://' to the URL: {url_to_shorten}")
            
        shorten_url(url_to_shorten)
    else:
        print("Input cannot be empty. Exiting.")
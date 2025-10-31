import urllib.robotparser
from urllib.parse import urljoin, urlparse
import sys

def check_robots_exclusion(base_url, path_to_check, user_agent):
    """
    checks the robots.txt file of a website to see if a path is allowed
    for a given User-Agent.
    """
    if not base_url.startswith('http'):
        print("\n Error: Base URL must start with 'http://' or 'https://'.")
        return

    # this uses the base URL to find the location of robots.txt
    rp = urllib.robotparser.RobotFileParser()
    robots_url = urljoin(base_url, '/robots.txt')
    rp.set_url(robots_url)
    
    print(f"Fetching robots.txt from: {robots_url}...")
    
    try:
        # fetches and parse the robots.txt file
        rp.read()
    except Exception as e:
        print(f"\n Error: Could not read robots.txt. Site may not have one or connectivity issue. ({e})")
        return

    # Check if the User-Agent is allowed to fetch the URL path
    # NOTE: The path_to_check must be a relative path from the domain root.
    # The urllib.robotparser automatically converts the path to be absolute 
    # based on its set_url, but we should ensure the user input looks like a path.
    if not path_to_check.startswith('/'):
        path_to_check = '/' + path_to_check
        
    is_allowed = rp.can_fetch(user_agent, path_to_check)
    
    status = "ALLOWED" if is_allowed else "DISALLOWED"
    status_emoji = "✅" if is_allowed else "❌"

    print("\n Robots.txt Check Result ")
    print(f"Site: {base_url}")
    print(f"User-Agent: {user_agent}")
    print(f"Path to Check: {path_to_check}")
    print(f"Status: {status_emoji} **{status}**")
    print("\n")

if __name__ == "__main__":
    print(" Robots Exclusion Protocol Checker ")
    
    # gets the  inputs
    base_url = input("Enter website root URL (e.g., https://www.google.com): ").strip()
    path = input("Enter the path to check (e.g., /search, /private/): ").strip()
    user_agent = input("Enter User-Agent (e.g., Googlebot, *): ").strip()
    
    if base_url and path and user_agent:
        check_robots_exclusion(base_url, path, user_agent)
    else:
        print("All inputs are required. Exiting.")
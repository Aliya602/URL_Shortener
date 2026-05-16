""" Advanced URL Shortner"""

import requests # Allows making web requests to the TinyURL API
from colorama import Fore, Style, init
init()
import pyperclip # type: ignore # For copying the shortened URL to clipboard
import json 
from datetime import datetime


print('='*50)
print(Fore.LIGHTGREEN_EX + 'URL Shortener' + Style.RESET_ALL)
print('='*50)

# location to save the history of shortened URLs
HISTORY_FILE = 'url_shortener_history.json'

# Function to load history from the JSON file
def load_history():
    try:
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Function to save history to the JSON file
def save_history(history_list):
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history_list, f, indent=2)

def shorten_url(long_url):
    url = 'https://tinyurl.com/api-create.php'
    data = {'url': long_url}
    
    try:
        response = requests.post(url, data=data, timeout=10) # Set a timeout for the request
        if response.status_code == 200:
            return response.text
        else:
            return None
    except requests.RequestException as e:
        print(Fore.RED + f'Error shortening URL: {e}' + Style.RESET_ALL)
        return None

# Function to validate and format the URL
def validate_url(url):
    if not url:
        return False
    
    # Add https:// if missing
    if not url.startswith(('http://', 'https://')):
        return 'https://' + url
    return url  

# Function to show users history
def show_history(history):
    if not history:
        print(Fore.YELLOW + 'No URL shortened history found.' + Style.RESET_ALL)
        return
    
    print(Fore.LIGHTYELLOW_EX + '📋Shortened URL History:' + Style.RESET_ALL)
    print('-'*50)
    for i, item in enumerate(history[-10:], 1):  # Show last 10 entries
        print(f'{i}. Original: {item["original"][:50]}...')
        print(f'   Shortened: {item["shortened"]}')
        print(f'   Date: {item["date"]}')
        print('-'*50)
 
# Main program
history_load = load_history()

while True:
    print('\n' + '='*50)
    print(Fore.LIGHTBLUE_EX + '📍OPTIONS:' + Style.RESET_ALL)
    print('1. Shorten a new URL')
    print('2. View shortened URL history')
    print('3. Clear history')
    print('4. Exit')
    print('='*50)

# if statment to handle user choices
    choice = input('Enter your choice (1-4): ')
    if choice == '1':
        long_url = input('\n' + Fore.CYAN + '📎 Enter the long URL to shorten: ' + Style.RESET_ALL)

        long_url = validate_url(long_url)
        if not long_url:
            print(Fore.RED + 'Invalid URL. Please try again.' + Style.RESET_ALL)
            continue 

        print(Fore.YELLOW + '⌚Shortening URL...' + Style.RESET_ALL)
        short_url = shorten_url(long_url)
        if short_url:
            print(Fore.GREEN + f'✅ Shortened URL: {short_url}' + Style.RESET_ALL)
            pyperclip.copy(short_url) # Copy the shortened URL to clipboard
            print(Fore.LIGHTGREEN_EX + '📋 Shortened URL copied to clipboard!' + Style.RESET_ALL)

            # Save to history
            history_load.append({
                'original': long_url,
                'shortened': short_url,
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            save_history(history_load)
        
        else:
            print(Fore.RED + '❌Error shortening URL. Please try again.' + Style.RESET_ALL)

    elif choice == '2':
        show_history(history_load)

    elif choice == '3':
        confirm = input(Fore.RED + 'Are you sure you want to clear history? (y/n): ' + Style.RESET_ALL)
        if confirm.lower() == 'y':
            history_load = []
            save_history(history_load)
            print(Fore.GREEN + '✅History cleared successfully!' + Style.RESET_ALL)

    elif choice == '4':
        print(Fore.GREEN + f'Goodbye 👋! You shortened {len(history_load)} URLs' + Style.RESET_ALL)
        break
    else:
        print(Fore.RED + 'Invalid choice. Please enter a number between 1 and 4.' + Style.RESET_ALL)



 




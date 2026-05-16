
"""Simple URL Shortener using TinyURL API"""

import requests # Allows making web requests to the TinyURL API
from colorama import Fore, Style, init
init()

print('='*50)
print(Fore.LIGHTGREEN_EX + 'URL Shortener' + Style.RESET_ALL)
print('='*50)

long_url = input('Enter the long  URL to shorten: ')

url = 'https://tinyurl.com/api-create.php'

data = {'url': long_url}
response = requests.post(url, data=data)

if response.status_code == 200:
    short_url = response.text
    print(Fore.GREEN + f'Shortened URL: {short_url}' + Style.RESET_ALL)
else:
    print(Fore.RED + 'Error shortening URL. Please try again.' + Style.RESET_ALL)
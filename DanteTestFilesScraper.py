import requests
from bs4 import BeautifulSoup
import sys
import os


def get_page_html(url: str):
    """Download page HTML and return BeautifulSoup object"""
    try:
        r = requests.get(url)
    except:
        print("Error: Can't download HTML from " + url)
        exit()
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def get_files_links_and_names(soup: BeautifulSoup):
    """Return dictionary with file names as keys and links as values"""
    links = {}
    try:
        for link in soup.select('div[id="sec9-body"] p.codel a'):
            links.update({link.text: link.get('href')})
    except:
        print("Error: Can't find links on page")
        exit()
    return links

def download_file(url: str, file_name: str, dest: str = os.getcwd()):
    """Download file from url and save it as file_name in dest directory (default is current directory)"""
    try:
        r = requests.get(url, allow_redirects=True)
    except:
        print("Error: Can't download file from " + url)
        exit()
    with open(os.path.join(dest, file_name), 'wb') as f:
        f.write(r.content)
        f.close()

# Check if script was called with -h flag or without any arguments
if len(sys.argv) - 1 == 0 or sys.argv[1] == "-h":
    print(f"Syntax: python DanteTestFilesScraper.py [-h] <URL>\n\n<URL> - Address of the Dante's tasks report page\n\nFlag    Action\n-h       Show this help message and exit")
    exit()

# Get URL from command line arguments
url = sys.argv[1]
# Remove index.html from URL
urlWithoutIndex = url[:-10]
soup = get_page_html(url)
links = get_files_links_and_names(soup)
# Download files
for file_name, link in links.items():
    print("Downloading: " + file_name)
    download_file(urlWithoutIndex+link, file_name)


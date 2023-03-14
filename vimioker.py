import requests
import argparse
import os
from bs4 import BeautifulSoup
from termcolor import colored
from tqdm import tqdm
import random
import time



def print_banner():
    """
    Prints a banner with the name of the tool, a brief description, and usage information.
    """
    banner = [
        '===============================================================================',
        '',
        ' ██╗   ██╗██╗███╗   ███╗██╗ ██████╗ ██╗  ██╗███████╗██████╗ ',
        ' ██║   ██║██║████╗ ████║██║██╔═══██╗██║ ██╔╝██╔════╝██╔══██╗',
        ' ██║   ██║██║██╔████╔██║██║██║   ██║█████╔╝ █████╗  ██████╔╝',
        ' ╚██╗ ██╔╝██║██║╚██╔╝██║██║██║   ██║██╔═██╗ ██╔══╝  ██╔══██╗',
        '  ╚████╔╝ ██║██║ ╚═╝ ██║██║╚██████╔╝██║  ██╗███████╗██║  ██║',
        '   ╚═══╝  ╚═╝╚═╝     ╚═╝╚═╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝',
        '',
        'A powerful web scraper for hackers and malicious coders.',
        '',
        'Usage: python pyscramte.py [-h] [-d DIRECTORY] [-t TIMEOUT] [-v] url',
        '',
        'Arguments:',
        '',
        '  url                  URL to scrape',
        '',
        'Optional arguments:',
        '',
        '  -h, --help           Show this help message and exit',
        '  -d DIRECTORY, --directory DIRECTORY',
        '                       Directory to save output files (default: current directory)',
        '  -t TIMEOUT, --timeout TIMEOUT',
        '                       Timeout in seconds for HTTP requests (default: 10)',
        '  -v, --verbose        Enable verbose mode',
        '',
        'Created by Dismantle',
        '==============================================================================='
    ]

    # Define the color scheme for the banner text
    colors = [
        'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white'
    ]

    # Set the speed of scrolling
    delay = 0.02

    # Print each line of the banner with a random color and delay
    for line in banner:
        color = random.choice(colors)
        for char in line:
            print(colored(char, color), end='', flush=True)
            time.sleep(delay)
        print()


# Configure argparse
parser = argparse.ArgumentParser(description="Web scraper tool for hackers and malicious coders")
parser.add_argument("-f", "--file", help="File containing URLs to scrape")
parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode")
parser.add_argument("-o", "--output", help="Output file name")
parser.add_argument("-s", "--scrape-hidden", action="store_true", help="Scrape hidden directories")
args = parser.parse_args()

# Configure headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

# Function to scrape URLs
def scrape_url(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup

# Function to get directory path from URL
def get_directory_path(url):
    if url.endswith("/"):
        return url[:-1]
    return url[:url.rfind("/") + 1]

# Function to get file name from URL
def get_file_name(url):
    return url[url.rfind("/") + 1:]

# Function to get all links from a page
def get_links(url):
    soup = scrape_url(url)
    links = []

    for link in soup.find_all("a"):
        link_url = link.get("href")
        if link_url and not link_url.startswith("http"):
            if link_url.startswith("/") and not link_url.startswith("//"):
                link_url = get_directory_path(url) + link_url[1:]
            else:
                link_url = get_directory_path(url) + link_url
            links.append(link_url)

    return links

# Function to scrape a directory
def scrape_directory(url, scrape_hidden):
    output = []

    # Get links from directory
    links = get_links(url)

    # Scrape each link
    for link in links:
        if not scrape_hidden and link.startswith(get_directory_path(url) + "."):
            continue
        if link.endswith("/"):
            # Scrape subdirectory
            output.extend(scrape_directory(link, scrape_hidden))
        else:
            # Scrape file
            file_name = get_file_name(link)
            response = requests.get(link, headers=headers)
            content = response.content
            with open(file_name, "wb") as f:
                f.write(content)
            output.append(f"Saved file {file_name}")

    return output

def print_output(output):
    border = colored("+" + "-" * 78 + "+", "magenta")
    for o in output:
        box = "\n".join(["| " + line.ljust(76) + " |" for line in o.split("\n")])
        print(f"\n{border}\n{box}\n{border}\n")

def write_output(output, file_name):
    with open(file_name, "w") as f:
        border = colored("+" + "-" * 78 + "+\n", "blue")
        for o in output:
            box = "\n".join(["| " + line.ljust(76) + " |" for line in o.split("\n")])
            f.write(f"{border}{box}\n{border}\n")

# Main function to scrape URLs
def main():
    urls = []
    if args.file:
        with open(args.file, "r") as f:
            urls = [line.strip() for line in f]
    else:
        urls = args.url

    output = []

    # Scrape each URL
    for url in urls:
        output.append(f"Scraping {url}...")
        if url.endswith("/"):
            # Scrape directory
            output.extend(scrape_directory(url, args.scrape_hidden))
        else:
            # Scrape file
            file_name = get_file_name(url)
            response = requests.get(url, headers=headers)
            content = response.content
            with open(file_name, "wb") as f:
                f.write(content)
            output.append(f"Saved file {file_name}")

    # Print or write output to file
    if args.output:
        write_output(output, args.output)
    else:
        print_output(output)

# Check verbose mode
if args.verbose:
    print(colored("Running in verbose mode", "yellow"))

# Call main function
if __name__ == "__main__":
    main()

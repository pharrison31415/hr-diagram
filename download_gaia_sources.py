import os
import requests
import sys
from urllib.parse import urljoin

from bs4 import BeautifulSoup


def get_source_urls(count):
    url = "https://cdn.gea.esac.esa.int/Gaia/gdr2/gaia_source/csv/"
    response = requests.get(url)

    # Extract href values
    soup = BeautifulSoup(response.content, "html.parser")
    links = [a["href"] for a in soup.find_all("a", href=True)]

    # Filter to only have GaiaSource filenames
    all_source_filenames = filter(lambda a: "GaiaSource" in a, links)

    # Grab first <count>
    source_filenames = list(all_source_filenames)[:count]

    # Create full source urls
    source_urls = [urljoin(url, filename) for filename in source_filenames]

    return source_urls


def download_to_dir(source_urls, directory):
    # Make sure the directory exists, if not, create it
    if not os.path.exists(directory):
        os.makedirs(directory)

    for i, url in enumerate(source_urls):
        print(f"Downloading {i+1} of {len(source_urls)}")
        # Get the filename from the URL (the last part of the URL)
        filename = url.split('/')[-1]
        file_path = os.path.join(directory, filename)

        try:
            response = requests.get(url)
            response.raise_for_status()

            # Write the content to a file
            with open(file_path, 'wb') as file:
                file.write(response.content)

        except requests.exceptions.RequestException as e:
            print(f"Error downloading {url}: {e}")


def main():
    # Verify we have a directory arg
    if len(sys.argv) < 2:
        print("A directory to download to must be provided.", file=sys.stderr)
        sys.exit(1)
    directory = sys.argv[1]

    # Specify number of urls to grab for downloading
    count = 5
    if len(sys.argv) == 3:
        count = int(sys.argv[2])

    # Scrape page for source urls
    source_urls = get_source_urls(count)

    # Download and save
    download_to_dir(source_urls, directory)


if __name__ == "__main__":
    main()

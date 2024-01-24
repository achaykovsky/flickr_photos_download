import os
import logging
import argparse
import requests
from flickrapi import FlickrAPI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_arguments():
    # Create argument parser
    parser = argparse.ArgumentParser(description='Downloading photos from Flickr')

    # Add arguments
    parser.add_argument('tags', nargs='+', type=str)
    parser.add_argument('count', type=int, default=1)
    parser.add_argument('date', type=str, default='2023-01-01')

    # Parse the arguments
    args = parser.parse_args()

    tags = args.tags
    count = args.count
    date = args.date

    # Access and use the arguments
    logging.info("tags:", tags)
    logging.info("count:", count)
    logging.info("date:", date)
    return tags, count, date


def authenticate(api_key, api_secret):
    """Authenticate with Flickr API."""
    return FlickrAPI(api_key, api_secret, format='parsed-json')


def download_image_from_url(url, destination):
    response = requests.get(url)

    if response.status_code == 200:
        with open(destination, 'wb') as file:
            file.write(response.content)
        logging.info(f"Image downloaded successfully to {destination}")
    else:
        logging.error(f"Failed to download image. Status code: {response.status_code}")


def download_photo(photo, download_dir):
    """Download a single photo."""
    try:
        # Construct the photo URL with the optional port number
        photo_url = f"http://farm{photo['farm']}.staticflickr.com/{photo['server']}/{photo['id']}_{photo['secret']}.jpg"

        photo_title = photo['title']

        file_path = os.path.join(download_dir, f"{photo_title}.jpg")

        download_image_from_url(photo_url, file_path)

        logger.info(f"Downloaded: {photo_title}")

    except Exception as e:
        logger.error(f"Error downloading photo {photo['title']}: {e}")


def retrieve_photos_by_tag(flickr, tag, date, count, download_dir, per_page=10, page=1):
    """Retrieve photos from Flickr based on a specific tag with pagination."""
    total_pages = 1
    counter = 0

    try:
        while page <= total_pages and counter < count:
            # Make the API call to get photos based on the specified tag for the current page
            photos = flickr.photos.search(tags=tag, min_upload_date=date, per_page=per_page, page=page,
                                          sort='date-posted-desc', content_types=0)

            # Update the total number of pages (if not already updated)
            if total_pages == 1:
                total_pages = photos['photos']['pages']

            # Download each photo
            for photo in photos['photos']['photo']:
                download_photo(photo, download_dir)
                counter += 1

            # Move to the next page
            page += 1
    except Exception as e:
        logger.error(f"Error retrieving photos by tag: {e}")


def create_output_directory():
    current_directory = os.getcwd()
    path = current_directory + '\\downloads\\'
    download_dir = os.path.join(current_directory, path)
    os.makedirs(download_dir, exist_ok=True)
    return download_dir


if __name__ == "__main__":

    tags, count, date = get_arguments()

    API_KEY = os.environ.get("API_KEY")
    API_SECRET = os.environ.get("API_SECRET")

    # Set the directory to save downloaded images
    download_dir = create_output_directory()

    # Authenticate with Flickr API
    try:
        flickr = authenticate(API_KEY, API_SECRET)

        # Retrieve and download photos by tag with pagination
        retrieve_photos_by_tag(flickr, tags, date, count, download_dir, per_page=1, page=1)

        logger.info("Download complete.")
    except Exception as e:
        logger.error(f"Error: {e}")

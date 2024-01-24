# Flickr Photo Downloader

This script allows you to download photos from Flickr based on specified tags, count, and date criteria. It utilizes the Flickr API for photo retrieval and downloads the images to a specified directory.

## Prerequisites

Before running the script, make sure you have the following:

- Python installed (version 3.x)
- Required Python packages installed. You can install them using the following command:

  ```bash
  pip install flickrapi requests
  ```

- Flickr API key and secret. You can obtain them by creating a [Flickr App](https://www.flickr.com/services/apps/create/) and setting up your API key and secret as environment variables (`API_KEY` and `API_SECRET`).

## Usage

Run the script from the command line with the following arguments:

```bash
python scrape.py <tags> <count> <date>
```

- `tags`: One or more space-separated tags to filter photos.
- `count`: The number of photos to download (default=1)
- `date`: The minimum upload date for retrieved photos (format: 'YYYY-MM-DD'), (default='2023-01-01').

Example:

```bash
python scrape.py cat 5 2023-01-01
```

## Output

The downloaded photos will be saved in the 'downloads' directory within the script's current working directory. Each photo is named based on its title.

## Environment Variables

Ensure that you have set the following environment variables before running the script:

- `API_KEY`: Your Flickr API key.
- `API_SECRET`: Your Flickr API secret.

## Logging

The script logs information and errors to the console. Successful downloads and any encountered errors will be displayed in the console output.

## Disclaimer

This script is provided as-is and is subject to the terms of the [MIT License](LICENSE). Use it responsibly and adhere to Flickr's [API Terms of Use](https://www.flickr.com/services/developer/api/).

**Note:** Ensure that you have read and understood Flickr's terms and conditions before using this script, and comply with their guidelines regarding API usage and content downloading.

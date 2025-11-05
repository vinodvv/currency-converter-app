import requests
import csv
import os
from datetime import datetime
from dotenv import load_dotenv

# Load .env values if present
load_dotenv()

# paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "log.txt")
OUTPUT_FILENAME = os.path.join(BASE_DIR, "output", "gbp_inr_rates.csv")

# Logging helper
def log(message):
    with open(LOG_FILE, "a") as file:
        file.write(f"{datetime.now()} - {message}\n")


# --- Configuration ---
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    log("❌ ERROR: API KEY environment variable not set. Script stopped.")
    exit(1)


BASE_CURRENCY = "GBP"
TARGET_CURRENCY = "INR"
API_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{BASE_CURRENCY}"
OUTPUT_FILENAME = "output/gbp_inr_rates.csv"


# --- Functions ---
def get_gbp_inr_rate(api_url):
    """
    Fetches the latest GBP to INR conversion rate and the update date from the API.

    Args:
        api_url: The URL for the exchange rate API.

    Returns:
        A tuple containing the GBP to INR rate (float) and the update date (str)
        in 'YYYY-MM-DD' format, or None if an error occurs.
    """
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        data = response.json()

        rate = data["conversion_rates"].get(TARGET_CURRENCY)
        if rate is None:
            # print(f"Error: {TARGET_CURRENCY} not found in conversion rates.")
            log(f"❌ ERROR: {TARGET_CURRENCY} not found in response.")
            return None

        # Extracting and reformatting the date to 'DD-MM-YYYY'
        date_utc_str = data["time_last_update_utc"]
        # Example format: "Thu, 01 Jun 2023 00:00:01 +0000"
        # We need to parse it and then format it as 'YYYY-MM-DD'
        # The API's date format is somewhat inconsistent in examples, assuming standard UTC format
        # If the format is 'YYYY-MM-DD HH:MM:SS', then slicing might work.
        # Let's use datetime parsing for robustness.
        try:
            # Attempt to parse a common UTC string format
            date_obj = datetime.strptime(date_utc_str, "%a, %d %b %Y %H:%M:%S %z")
        except ValueError:
            # Fallback for simpler UTC string like "YYYY-MM-DD HH:MM:SS"
            date_obj = datetime.strptime(date_utc_str, "%Y-%m-%d %H:%M:%S")

        formatted_date = date_obj.strftime("%d-%m-%Y")

        return rate, formatted_date

    # except requests.exceptions.RequestException as e:
    #     print(f"Error fetching data from API: {e}")
    #     return None
    # except KeyError as e:
    #     print(f"Error parsing API response: Missing key {e}")
    #     return None
    # except ValueError as e:
    #     print(f"Error processing date or JSON: {e}")
    #     return None
    except Exception as e:
        log(f"❌ ERROR: Fetching API data: {e}")


def write_to_csv(filename, date, rate):
    """
    Writes the conversion rate and date to a CSV file.
    Creates the file with headers if it doesn't exist.

    Args:
        filename: The path to the CSV file.
        date: The date of the conversion rate.
        rate: The conversion rate.
    """
    # Ensure the output directory exists
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        file_exists = os.path.exists(filename)

        with open(filename, "a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Date", f"{BASE_CURRENCY}_{TARGET_CURRENCY}"])
            writer.writerow([date, rate])
        # print(f"Successfully wrote {BASE_CURRENCY}/{TARGET_CURRENCY} rate ({rate}) for {date} to {filename}")
        log(f"CSV updated successfully. {BASE_CURRENCY}/{TARGET_CURRENCY} rate ({rate}) for {date} to {filename}")
    # except IOError as e:
    #     print(f"Error writing to CSV file {filename}: {e}")
    except Exception as e:
        log(f"❌ ERROR writing CSV: {e}")


# --- Main execution ---
if __name__ == "__main__":
    log("----- Script started -----")
    gbp_inr_data = get_gbp_inr_rate(API_URL)

    if gbp_inr_data:
        rate, date = gbp_inr_data
        write_to_csv(OUTPUT_FILENAME, date, rate)
    else:
        # print("Failed to retrieve GBP to INR conversion rate. CSV not updated.")
        log("❌ No data retrieved - CSV not updated.")

import requests
import csv
import os
import argparse
from datetime import datetime


# Functions
def get_exchange_rate(api_key, base, target):
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        rate = data["conversion_rates"].get(target)
        if rate is None:
            print(f"Error: {target} not found in conversion rates.")
            return None

        date_utc_str = data["time_last_update_utc"]
        try:
            date_obj = datetime.strptime(date_utc_str, "%a, %d %b %Y %H:%M:%S %z")
        except ValueError:
            date_obj = datetime.strptime(date_utc_str, "%Y-%m-%d %H:%M:%S")

        formatted_date = date_obj.strftime("%d-%m-%Y")
        return rate, formatted_date

    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return None

    except (KeyError, ValueError) as e:
        print(f"Data parsing error: {e}")
        return None


def write_to_csv(filename, date, rate, base, target):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    file_exists = os.path.exists(filename)

    try:
        with open(filename, "a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Date" f"{base}_{target}"])
            writer.writerow([date, rate])
        print(f"✅ {base}/{target} rate ({rate}) for {date} saved to {filename}")

    except IOError as e:
        print(f"File write error: {e}")


# CLI setup
def main():
    parser = argparse.ArgumentParser(
        description="📈 Currency Converter CLI - Fetch exchange rate and store to CSV"
    )
    parser.add_argument(
        "--base", "-b", default="GBP", help="Base currency (default: GBP)"
    )
    parser.add_argument(
        "--target", "-t", default="INR", help="Target currency (default: INR)"
    )
    parser.add_argument(
        "--output", "-o", default="output/exchange_rates.csv",
        help="Output CSV file path (default: output/exchange_rates.csv)"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Only display the rate, don't save to file"
    )

    args = parser.parse_args()
    api_key = os.getenv("API_KEY")

    if not api_key:
        print("❌ Error: API_KEY environment variable is not set.")
        return

    rate_data = get_exchange_rate(api_key, args.base.upper(), args.target.upper())

    if rate_data:
        rate, date = rate_data
        print(f"💱 {args.base.upper()} → {args.target.upper()} rate on {date}: {rate}")
        if not args.dry_run:
            write_to_csv(args.output, date, rate, args.base.upper(), args.target.upper())

    else:
        print("❌ Failed to fetch exchange rate.")


if __name__ == "__main__":
    main()

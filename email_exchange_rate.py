import requests
import os
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage
from datetime import datetime


def load_credentials():
    load_dotenv()
    api_key = os.getenv("API_KEY")
    email_address = os.getenv("EMAIL_ADDRESS")
    email_password = os.getenv("EMAIL_PASSWORD")
    return api_key, email_address, email_password


def get_gbp_inr_rate(api_url):
    response = requests.get(API_URL)
    response.raise_for_status()
    data = response.json()

    rate = data["conversion_rates"].get(TARGET_CURRENCY)
    if rate is None:
        print(f"Error: {TARGET_CURRENCY} not found in conversion rates.")

    date_utc_str = data["time_last_update_utc"]
    try:
        date_obj = datetime.strptime(date_utc_str, "%a, %d %b %Y %H:%M:%S %z")
    except ValueError:
        date_obj = datetime.strptime(date_utc_str, "%Y-%m-%d %H:%M:%S")

    formatted_date = date_obj.strftime("%Y-%m-%d")
    return rate, formatted_date


def login_to_email(email_address, email_password):
    smtp = smtplib.SMTP("smtp.gmail.com", 587)
    smtp.starttls()
    smtp.login(email_address, email_password)
    return smtp


def create_email():
    msg = EmailMessage()
    msg['Subject'] = "💱 Today's GBP INR Exchange Rate"
    msg['From'] = "Vinod Valiyaveedu Vijayan"
    msg["To"] = "sreevnd@gmail.com"
    msg.set_content(f"Hi Jayasree,\n\n"
                    f"Today's GBP INR Exchange Rate\n"
                    f"💱 {BASE_CURRENCY} → {TARGET_CURRENCY} rate on {date}: {rate}\n\n"
                    f"Regards,\n\n"
                    f"Vinod V V")
    return msg


if __name__ == "__main__":
    api_key, email_address, email_password = load_credentials()
    BASE_CURRENCY = "GBP"
    TARGET_CURRENCY = "INR"
    API_URL = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{BASE_CURRENCY}"
    rate, date = get_gbp_inr_rate(API_URL)
    smtp = login_to_email(email_address, email_password)
    msg = create_email()
    smtp.send_message(msg)
    # print("Email sent successfully.")

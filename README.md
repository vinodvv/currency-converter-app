# 💱 Currency Converter App (GBP to INR)

This Python app fetches the latest exchange rate from GBP to INR using the [ExchangeRate-API](https://www.exchangerate-api.com/), and stores the rate in a CSV file for daily tracking.

## 📦 Features
- Fetches live exchange rates from GBP to INR
- Automatically formats and saves rates to a CSV
- Logs the date and rate in a persistent file
- Robust error handling

## 🚀 Usage

1. Set your API key as an environment variable:
   ```bash
   export API_KEY=your_api_key_here
    ```
2. Run the app:
    ```bash
    python currency_converter.py
    ```
3. Output will be saved to: output/gbp_inr_rates.csv

## 🧾 Requirements
Python 3.x

requests module

Install requirements:
```bash
pip install requests
```
## 📁 Project Structure
```bash
currency-converter/
│
├── currency_converter.py
├── output/
│   └── gbp_inr_rates.csv
├── .gitignore
├── README.md
└── LICENSE
```

## 🔧 Command-Line Usage

### Run the script directly from the terminal
```bash
python currency_converter.py --base USD --target EUR
```

### Options
* --base, -b: Base currency (default: GBP)
* --target, -t: Target currency (default: INR)
* --output, -o: Output CSV path (default: output/exchange_rates.csv)
* --dry-run: Print exchange rate without saving

### Example
```bash
python currency_converter.py -b EUR -t INR --dry-run
```

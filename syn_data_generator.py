import pandas as pd
import random
import sys
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

def main():
    # --- Argument Validation ---
    if len(sys.argv) < 3:
        sys.exit("Too few command-line arguments. Usage: python synthetic_campaign_data.py <num_campaigns> (--csv | --sheet)")
    if len(sys.argv) > 3:
        sys.exit("Too many command-line arguments. Usage: python synthetic_campaign_data.py <num_campaigns> (--csv | --sheet)")

    num_campaigns = sys.argv[1]
    save_option = sys.argv[2].lower()

    if not num_campaigns.isdigit():
        sys.exit("Usage: <num_campaigns> must be an integer.")
    if save_option not in ["--csv", "--sheet"]:
        sys.exit("Usage: Specify either --csv or --sheet as the second argument.")

    num_campaigns = int(num_campaigns)

    # --- Generate Synthetic Data ---
    df = syn_data_generator(num_campaigns)
    print(f"✅ Generated {num_campaigns} synthetic campaigns.")

    # --- Save or Upload Based on Flag ---
    if save_option == "--csv":
        save_to_csv(df)
    elif save_option == "--sheet":
        upload_to_google_sheets(df)


def syn_data_generator(num_campaigns):
    """Generates synthetic ad campaign performance data."""
    campaign_types = ["Summer Sale", "Brand Awareness", "Retargeting", "Search", "Product Launch", "Holiday Promo"]
    platforms = ["Google Ads", "Facebook Ads", "Instagram", "TikTok", "LinkedIn", "Twitter", "YouTube"]

    data = []
    for _ in range(num_campaigns):
        campaign_type = random.choice(campaign_types)
        platform = random.choice(platforms)
        campaign_name = f"{campaign_type} - {platform}"

        impressions = random.randint(10_000, 100_000)
        ctr = round(random.uniform(1.0, 5.0), 2)
        clicks = int(impressions * (ctr / 100))
        conversions = max(1, int(clicks * random.uniform(0.02, 0.15)))
        cost = round(clicks * random.uniform(1.0, 3.0), 2)
        cpa = round(cost / conversions, 2) if conversions > 0 else None

        data.append({
            "campaign_name": campaign_name,
            "platform": platform,
            "clicks": clicks,
            "impressions": impressions,
            "conversions": conversions,
            "cost": cost,
            "ctr_%": ctr,
            "cpa_$": cpa
        })

    return pd.DataFrame(data)


def save_to_csv(df):
    """Saves DataFrame locally as CSV."""
    filename = "synthetic_campaign_data.csv"
    df.to_csv(filename, index=False)
    print(f"💾 Saved locally as {filename}")


def upload_to_google_sheets(df):
    """Uploads DataFrame to Google Sheets using API credentials."""

   # --- Placeholders to Replace ---
    SERVICE_ACCOUNT_FILE = "<your_service_account.json>"
    SPREADSHEET_ID = "<spreadsheet_id>"
    SHEET_NAME = "<sheet_name>"

    # --- Authenticate ---
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets", 
              "https://www.googleapis.com/auth/drive"]

    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()

    # --- Prepare Data ---
    values = [df.columns.tolist()] + df.values.tolist()

    # --- Upload Data ---
    request = sheet.values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{SHEET_NAME}!A1",
        valueInputOption="RAW",
        body={"values": values}
    )
    request.execute()

    print(f"☁️ Uploaded to Google Sheets ({SHEET_NAME}) successfully!")

if __name__ == "__main__":
    main()

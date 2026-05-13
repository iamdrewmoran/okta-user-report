import truststore
truststore.inject_into_ssl()

import requests
import csv
import os
from dotenv import load_dotenv


def setup():
    """Loads credentials from .env and returns the domain and headers."""
    load_dotenv()
    domain = os.getenv("OKTA_DOMAIN")
    api_token = os.getenv("OKTA_API_TOKEN")
    headers = {
        "Authorization": f"SSWS {api_token}",
        "Accept": "application/json"
    }
    return domain, headers


def get_all_users(domain, headers):
    """Fetches all users from Okta, handling pagination."""
    all_users = []
    url = f"https://{domain}/api/v1/users"

    while url:
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            break

        all_users.extend(response.json())
        print(f"Retrieved {len(all_users)} users so far...")

        links = response.links
        url = links["next"]["url"] if "next" in links else None

    print(f"\nTotal users retrieved: {len(all_users)}")
    return all_users


def write_user_report(all_users, filename):
    """Writes the Okta user data to a CSV file."""
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Full Name", "Username", "Email", "Market", "Department", "Salesforce Role", "Location", "Job Title", "Status"])

        for user in all_users:
            profile = user.get("profile", {})
            full_name = f"{profile.get('firstName', '')} {profile.get('lastName', '')}"
            writer.writerow([
                full_name,
                profile.get("samAccountName", ""),
                profile.get("email", ""),
                profile.get("market", ""),
                profile.get("department", ""),
                profile.get("rolesSalesForce", ""),
                profile.get("physicalDeliveryOffice", ""),
                profile.get("title", ""),
                user.get("status", "")
            ])

    print(f"Report saved to {filename}")


# --- Main execution ---
domain, headers = setup()
users = get_all_users(domain, headers)
write_user_report(users, "okta_user_report.csv")
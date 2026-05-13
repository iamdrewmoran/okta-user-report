# Okta User Report

A Python script built for IAM automation that connects to the Okta API and exports a full user report to CSV. Handles pagination automatically to retrieve all users regardless of tenant size.

## What It Does

- Authenticates to Okta using a secure API token stored in a `.env` file
- Retrieves all users from your Okta tenant, handling pagination automatically
- Exports user data to a CSV file with the following default fields:
  - Full Name, Username, Email, Market, Department
  - Salesforce Role, Location, Job Title, Status
- Fields are fully interchangeable — simply update the column headers and `profile.get()` calls in `write_user_report()` to match any Okta user profile attributes your org uses

## Prerequisites

- Python 3.x
- The following Python packages:
```
  pip install requests python-dotenv truststore
```
- An Okta API token with read access to users

## Setup

1. Clone this repository:
```bash
   git clone https://github.com/iamdrewmoran/okta-user-report.git
   cd okta-user-report
```

2. Create a `.env` file in the project root with your Okta credentials:
```
   OKTA_DOMAIN=yourcompany.okta.com
   OKTA_API_TOKEN=your-token-here
```

3. Run the script:
```bash
   python user_report.py
```

## Output

Generates `okta_user_report.csv` in the project directory containing all users from your Okta tenant.

## Security Notes

- The `.env` file is listed in `.gitignore` and will never be committed to version control
- Never hardcode your API token directly in the script
- Restrict your Okta API token to specific network zones in the Okta Admin Console for additional security

## Tech Stack

- Python 3
- [Okta Users API](https://developer.okta.com/docs/api/openapi/okta-management/management/tag/User/)
- `requests` — HTTP requests to the Okta API
- `python-dotenv` — secure credential management
- `truststore` — SSL certificate handling for corporate VPN environments
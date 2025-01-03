# (c) 2025 Yonz
# License NonLicense
#
# This script updates a Cloudflare Access policy with your current public IP address.
# It assumes that the policy uses a simple IP range rule.
# Modify the script as needed to match your policy configuration.
#
# ##################### ATTENTION ####################
#
# Script is not working. the Method "client.zero_trust.access.policies.update" throws an unexpected error:
""" 
    Another non-200-range status code was received:404 <Response [404 Not Found]>
Error code: 404 - {'result': None, 'success': False, 'errors': [{'code': 12135, 'message': 'access.api.error.not_found'}], 'messages': []}

"""

import os
import time
import requests
from dotenv import load_dotenv
import cloudflare
from cloudflare import Cloudflare

load_dotenv()

# --- Replace with your actual values or set them as environment variables ---
API_TOKEN = os.getenv('CF_API_TOKEN', 'your-api-token')
API_KEY = os.getenv('CF_API_KEY', 'your-api-key')
EMAIL = os.getenv('CF_EMAIL', 'your-email') # only needed for API key authentication
ACCOUNT_ID = os.getenv('CF_ACCOUNT_ID', 'your-account-id')
POLICY_ID = os.getenv('CF_POLICY_ID', 'your-policy-id')


def get_public_ip():
    """Fetches your current public IP address."""
    try:
        response = requests.get('https://api.ipify.org')
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error getting public IP: {e}")
        return None

def update_cloudflare_access_policy(ip_address):
    """Updates the Cloudflare Access policy with the new IP address."""
    try:
        # Pick the Authentication Method. If a Token is defined, use it, otherwise use API Key and Email
        if API_TOKEN:
            client = Cloudflare(
                api_token=API_TOKEN
            )
        elif API_KEY and EMAIL:
            client = Cloudflare(
                api_key= API_KEY,
                api_email= EMAIL
            )    
        else:
            print("Please provide an API Token or API Key and Email")
            return

        print(f"Cloudflare Client: {client.api_email}")

        # Get the existing Access policy
        policy = client.zero_trust.access.policies.get(
            account_id=ACCOUNT_ID, 
            policy_id=POLICY_ID
            )
        print(f"Policy (Current): {policy.name} ip: {policy.include[0].ip}")

        # Update the policy if the IP address has changed
        # ip_address = '10.147.18.25' # Set to a different IP to test the update

        if policy.include[0].ip == f"{ip_address}/32":
            print("IP address has not changed. Exiting...")
        else:
            print(f"Updating policy ip to: {ip_address}/32")
            policy.include[0].ip = f"{ip_address}/32"
            # Update the policy
            PolicyUpdateResponse = client.zero_trust.access.policies.update(
                account_id=ACCOUNT_ID,
                policy_id=POLICY_ID,
                decision=policy.decision,  # Keep the existing decision
                name=policy.name,          # Keep the existing name
                include=[{"ip": f"{current_ip}/32"}]  # Update the include rule
                )
            print("Cloudflare Access policy updated successfully!")
            time.sleep(5) # Wait for the policy to be updated
            policy = client.zero_trust.access.policies.get(
                account_id=ACCOUNT_ID, 
                policy_id=POLICY_ID
                )
            print(f"Policy (after update): {policy.name} ip: {policy.include[0].ip}")
        # end if

    except cloudflare.APIConnectionError as e:
        print("The server could not be reached")
        print(e.__cause__)  # an underlying Exception, likely raised within httpx.
    except cloudflare.RateLimitError as e:
        print("A 429 status code was received; we should back off a bit.")
    except cloudflare.APIStatusError as e:
        print("Another non-200-range status code was received")
        print(e.status_code)
        print(e.response)
        print(e)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    current_ip = get_public_ip()
    if current_ip:
        update_cloudflare_access_policy(current_ip)

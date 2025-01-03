# cloudflare-tunnel-policy-update
Dynamic update of cloudflare IP-Address tunnel policy, 


This script updates a Cloudflare Access policy with your current public IP address.
It assumes that the policy uses a simple IP range rule.
Modify the script as needed to match your policy configuration.

## Prerequisits

Set the follwoing environment variables (e.g. in a _.env_ file):

For legacy authentication use the API Key and your E-Mail address
- `CF_API_KEY='your Cloudflare API Key'`
- `CF_EMAIL=admin@example.com`

For better control and security use API-Tokens with just enough rights to modify the Tunnel Policy
- `CF_API_TOKEN='Your API Token'`

Specify the Policy to change
- `CF_ACCOUNT_ID='Your Account ID'`
- `CF_POLICY_ID='Your Policy ID'`

The Script will log on to Cloudflare, fetch the current public IP Address, then update the specified tunnel. 

This is analog to a DynDNS Updater.



# meraki-api-reset-clientvpn-password

Summary:

This script silently resets Client VPN User password for each authorized user on
EVERY network associated with the Organization. Password for all users should be set to a complex passphrase. User will
not be notified of a password change, and will be forced to reset their password via Meraki web page.

Requirements:

1) Interpreter: Python 3.8.0+
2) Python Packages: meraki
3) API support for the Organization is enabled in Meraki Dashboard. Admins have generated their custom API keys.

How to run:

1) Open reset_client_password.py file with a text editor.
2) Configure your organization name, API Key, and new complex password for the vpn users under PARAMETERS section (Lines
   3-5).
3) Run python3 reset_clientvpn_password.py in the terminal. 
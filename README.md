dyndns-autologin	
=============
After the new dyndns ToS change you must login to your account once per month to keep it active.

This project is a Google Appengine project which will automatically login to your dyndns account to keep it active.
Please notice that this is probably agains the DynDns ToS. The author takes no responsibility if DynDns decides to ban your account

Installation
===================

- Change the application in app.yaml into your own app-id
- Change username and password into the Settings class in cron.py file
- the script automatically executes every Monday

LICENSE
===================
The project is licensed under MIT-license. See the LICENSE file for more details

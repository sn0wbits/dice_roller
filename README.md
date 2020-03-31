# Roller-Bot
#### For those playing D&D while in quarentine or simply while alone.
This is a dice roller for when you gotta play remotely and still wanna show your rolls off, it is connected to discord using a webhook.

To get the webhook from discord you need to:
1. Edit the channel you wish it to send messages to.
2. Click Webhooks and then Create Webhook.
3. Copy the URL and get the ID and token from it.

The layout of the link is as follows:
https://discordapp.com/api/webhooks/ID/TOKEN

Installation of requirements:
```
pip3 install discord.py
pip3 install requests
```
If you wish to not download the requirements then simply comment out / remove the imports and the call to the ``send_disc_msg()`` function at line 162.

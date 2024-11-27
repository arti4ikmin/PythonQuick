# This script is ued to quickly react to a message within a server (emoji name should be the same for everything)
# Designed for mspaint server

import requests
from urllib.parse import quote

def add_reaction(token, channel_id, message_id, emoji_name, emoji_id):
    emoji_string = f"{emoji_name}:{emoji_id}"
    encoded_emoji = quote(emoji_string)
    url = f'https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}/reactions/{encoded_emoji}/@me'
    headers = {
        'Authorization': f'{token}'
    }
    requests.put(url, headers=headers)

token = 'DISCORDTOKEN'
channel_id = 'CHANNEL ID'
message_id = 'MESSAGE ID'
emoji_name = "Content"

emoji_ids = [
    "1284249234983489587",
    "1284249255006965842",
    "1284249255737036811",
    "1284249256399474691",
    "1284249303065563206",
    "1284249308002127933",
    "1284249311697178686",
    "1284249312498552884",
    "1284249314935312385",
    "1284249318458523718",
    "1284249319347847260",
    "1284249325211353239",
    "1284249360388849716",
    "1284249365501710489",
    "1284249369599541308",
    "1284249374662070466",
    "1284249403519008879",
    "1284249611300765790",
    "1284249615775957074",
    "1284249620989345862",
    "1284249626014253128",
    "1284249645878612110",
    "1284249647828832276",
    "1284249649603154002",
    "1284249651419021323",
    "1284249701926961265",
    "1284249703206092810",
    "1284249704540147814",
    "1284249705383198720",
    "1284249795250360483"
]

for emoji_id in emoji_ids:
    add_reaction(token, channel_id, message_id, emoji_name, emoji_id)

import requests
import argparse
import os

def get_oauth_token(client_id, client_secret):
    url = "https://slack.com/api/oauth.v2.access"
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }
    response = requests.post(url, data=data)
    response_json = response.json()
    if response.status_code != 200 or not response_json.get("ok"):
        raise ValueError(f"Failed to obtain OAuth token: {response_json.get('error')}")
    return response_json["access_token"]

def send_slack_message(access_token, channel, message, image_url=None):
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "channel": channel,
        "text": message,
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": message
                }
            }
        ]
    }

    if image_url:
        payload["blocks"].append(
            {
                "type": "image",
                "image_url": image_url,
                "alt_text": "Image attachment"
            }
        )

    response = requests.post(url, headers=headers, json=payload)
    response_json = response.json()
    if response.status_code != 200 or not response_json.get("ok"):
        raise ValueError(f"Failed to send message to Slack: {response_json.get('error')}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Send a message to Slack with an optional image attachment using a Slack app.')
    parser.add_argument('--client-id', required=True, help='Slack app client ID')
    parser.add_argument('--client-secret', required=True, help='Slack app client secret')
    parser.add_argument('--channel', required=True, help='Slack channel ID or name to send the message')
    parser.add_argument('--text-message', required=True, help='Text message to send')
    parser.add_argument('--image-url', help='URL of the image attachment (optional)', default=None)

    args = parser.parse_args()

    # Obtain OAuth access token
    access_token = get_oauth_token(args.client_id, args.client_secret)

    # Send message to Slack
    send_slack_message(access_token, args.channel, args.text_message, args.image_url)

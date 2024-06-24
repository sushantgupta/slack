import requests
import argparse
import base64

def send_slack_message(webhook_url, message, image_file=None):
    # Read the message from the file
    with open(message, 'r') as file:
        message_text = file.read().strip()

    # Slack message payload
    payload = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": message_text
                }
            }
        ]
    }

    # If image_file is provided, read and encode the image
    if image_file:
        with open(image_file, 'rb') as file:
            image_data = base64.b64encode(file.read()).decode('utf-8')
        # Include the base64 image string in the payload as text (Slack will not render it as an image)
        payload["blocks"].append(
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"![Image](data:image/jpeg;base64,{image_data})"
                }
            }
        )

    response = requests.post(webhook_url, json=payload)

    if response.status_code != 200:
        raise ValueError(f'Request to Slack returned an error {response.status_code}, the response is:\n{response.text}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Send a message to Slack with an optional image attachment.')
    parser.add_argument('--webhook', required=True, help='Slack webhook URL')
    parser.add_argument('--text-message', required=True, help='Path to the message file')
    parser.add_argument('--image-file', help='Path to the image file (optional)', default=None)

    args = parser.parse_args()

    send_slack_message(args.webhook, args.text_message, args.image_file)

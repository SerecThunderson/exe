import asyncio
import json
from pyrogram import Client, errors
import os

def create_config():
    print("Creating a new config.json file.")
    api_id = input("Enter your api_id: ")
    api_hash = input("Enter your api_hash: ")
    destination_group_id = int(input("Enter your destination_group_id (a negative number): "))

    config_data = {
        "api_id": api_id,
        "api_hash": api_hash,
        "destination_group_id": destination_group_id,
        "error_wait_delay": 300  # Default error wait delay
    }

    with open("config.json", "w") as file:
        json.dump(config_data, file, indent=4)
    print("config.json saved <3")

# Check if config.json exists, if not, create it
if not os.path.exists("config.json"):
    create_config()

# Load configuration from config.json
with open("config.json", "r") as file:
    config = json.load(file)

api_id = config["api_id"]
api_hash = config["api_hash"]
destination_group_id = config["destination_group_id"]
error_wait_delay = config["error_wait_delay"]

# Prompt for message details
message_to_send = input("Enter the message you'd like to send: ")
message_limit = int(input("Enter the number of times you'd like to send the message: "))
send_interval_seconds = float(input("Enter the interval in seconds between messages: "))

async def send_message_periodically():
    app = Client("account", api_id=api_id, api_hash=api_hash)
    message_count = 0

    async with app:
        while message_count < message_limit:
            try:
                print(f"Sending message to group {destination_group_id}")
                await app.send_message(destination_group_id, message_to_send)
                message_count += 1
                await asyncio.sleep(send_interval_seconds)
            except Exception as e:
                print(f"Error occurred: {e}. Waiting for {error_wait_delay} seconds before retrying.")
                await asyncio.sleep(error_wait_delay)
        print("Message limit reached. Stopping.")

if __name__ == "__main__":
    asyncio.run(send_message_periodically())

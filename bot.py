import asyncio
from telethon import TelegramClient, events, Button
import random
import os
from config import CONFIG, AKANE_IMAGES  # Import from config.py
from pymongo import MongoClient
from datetime import datetime

# MongoDB setup
mongo_client = MongoClient(CONFIG["MONGO"]["URI"])
db = mongo_client.get_database("akanebot")
users_collection = db["users"]

def get_random_akane_image():
    """Select a random Akane image file from the list"""
    if not AKANE_IMAGES:
        return None
    image_filename = random.choice(AKANE_IMAGES)
    image_path = os.path.join("images", image_filename)
    if not os.path.exists(image_path):
        return None
    return image_path

async def main():
    """Main function to run the Telegram bot"""
    client = TelegramClient(
        'akane_bot_session',
        CONFIG["TELEGRAM"]["API_ID"],
        CONFIG["TELEGRAM"]["API_HASH"]
    )
    
    await client.start(bot_token=CONFIG["TELEGRAM"]["BOT_TOKEN"])

    @client.on(events.NewMessage(pattern='/start'))
    async def send_welcome_message(event):
        """Handle the /start command to send a welcome message with an Akane image and buttons"""
        user = event.sender
        user_id = user.id
        username = user.username or "Unknown"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Store user data in MongoDB
        user_data = {
            "user_id": user_id,
            "username": username,
            "timestamp": timestamp
        }
        users_collection.update_one(
            {"user_id": user_id},
            {"$set": user_data},
            upsert=True
        )

        # Get total number of users
        total_users = users_collection.count_documents({})

        # Send private group message to the owner
        owner_id = CONFIG["TELEGRAM"]["OWNER_ID"]
        message = (
            f"New user started the bot:\n"
            f"User ID: {user_id}\n"
            f"Username: @{username}\n"
            f"Time: {timestamp}\n"
            f"Total Users: {total_users}"
        )
        # Replace 'private_group_id' with the actual group ID
        private_group_id = -100123456789  # Replace with your private group ID
        try:
            await client.send_message(private_group_id, message)
        except Exception as e:
            print(f"Failed to send message to private group: {e}")

        # Fetch a random Akane image
        image_path = get_random_akane_image()
        if not image_path:
            await event.reply("❌ No Akane images available. Please add some images to the 'images' folder!")
            return

        # Welcome message as per your request
        welcome_message = (
            "Welcome to Akane Checker \n"
            "We hope you'll like our bot, explore premium for more amazing features.\n"
            "Owner: @Nehxl"
        )

        # Inline buttons as per your request
        buttons = [
            [
                Button.inline("Gates", b"gates"),
                Button.inline("Tools", b"tools")
            ],
            [
                Button.inline("Status", b"status"),
                Button.url("Join Channel", "https://t.me/AkaneUpdates")
            ]
        ]

        # Send the message with the Akane image and buttons
        await event.reply(
            welcome_message,
            file=image_path,
            buttons=buttons
        )

    # Handlers for button clicks (callback queries)
    @client.on(events.CallbackQuery(data=b"gates"))
    async def handle_gates(event):
        gates_message = (
            "Gateways ALPHA CHECKER Bot ✧\n"
            "--------------------------------\n"
            "• TOTAL: 48\n"
            "• Gateways On: 48 ✅\n"
            "• Gateways Off: 0 ❌\n"
            "• Gateways In Maintenance: 0 ⚠️\n"
            "--------------------------------\n"
            "Select the Gate that you like the most\n"
            "and which adapts to what you need! ⚠️"
        )
        buttons = [
            [
                Button.inline("Auth", b"auth"),
                Button.inline("Charge", b"charge"),
                Button.inline("Shopify", b"shopify")
            ],
            [
                Button.inline("Free U.", b"free_u"),
                Button.inline("Mass Mode", b"mass_mode"),
                Button.inline("Specials", b"specials")
            ],
            [
                Button.inline("Back ⬅️", b"back")
            ]
        ]
        await event.edit(gates_message, buttons=buttons)

    @client.on(events.CallbackQuery(data=b"tools"))
    async def handle_tools(event):
        await event.answer("Tools button clicked!")

    @client.on(events.CallbackQuery(data=b"status"))
    async def handle_status(event):
        await event.answer("Status button clicked!")

    @client.on(events.CallbackQuery(data=b"auth"))
    async def handle_auth(event):
        await event.answer("Auth gate selected!")

    @client.on(events.CallbackQuery(data=b"charge"))
    async def handle_charge(event):
        await event.answer("Charge gate selected!")

    @client.on(events.CallbackQuery(data=b"shopify"))
    async def handle_shopify(event):
        await event.answer("Shopify gate selected!")

    @client.on(events.CallbackQuery(data=b"free_u"))
    async def handle_free_u(event):
        await event.answer("Free U. gate selected!")

    @client.on(events.CallbackQuery(data=b"mass_mode"))
    async def handle_mass_mode(event):
        await event.answer("Mass Mode gate selected!")

    @client.on(events.CallbackQuery(data=b"specials"))
    async def handle_specials(event):
        await event.answer("Specials gate selected!")

    @client.on(events.CallbackQuery(data=b"back"))
    async def handle_back(event):
        image_path = get_random_akane_image()
        if not image_path:
            await event.reply("❌ No Akane images available. Please add some images to the 'images' folder!")
            return
        welcome_message = (
            "Welcome to Akane Checker \n"
            "We hope you'll like our bot, explore premium for more amazing features.\n"
            "Owner: @Nehxl"
        )
        buttons = [
            [
                Button.inline("Gates", b"gates"),
                Button.inline("Tools", b"tools")
            ],
            [
                Button.inline("Status", b"status"),
                Button.url("Join Channel", "https://t.me/AkaneUpdates")
            ]
        ]
        await event.edit(welcome_message, file=image_path, buttons=buttons)

    print("Akane Checker bot is running...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("Bot stopped by user")
    finally:
        loop.close()

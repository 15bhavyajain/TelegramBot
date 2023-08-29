from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

BOT_TOKEN = '6585779136:AAEktXO4eIU8G9B7lWbSJhjP4yvb6qE-VVU'
ADMINS = []
REWARDS = {}

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Welcome to the rewards bot!")

def fetch_admins(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    admins = context.bot.getChatAdministrators(chat_id)
    for admin in admins:
        ADMINS.append(admin.user.id)
    update.message.reply_text("Admin list updated.")

def add_admin(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id in ADMINS:
        admin_username = update.message.text.split()[1].replace("@", "")
        ADMINS.append(admin_username)
        update.message.reply_text(f"{admin_username} has been added as an admin.")
    else:
        update.message.reply_text("You are not authorized to perform this action.")

def add_reward(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id in ADMINS:
        text = update.message.text
        parts = text.split()
        if len(parts) == 3:
            username = parts[1].replace("@", "")
            reward_amount = int(parts[2])
            if username in REWARDS:
                REWARDS[username] += reward_amount
            else:
                REWARDS[username] = reward_amount
            update.message.reply_text("Reward added successfully.")
        else:
            update.message.reply_text("Invalid format. Use: /add_reward <username> <reward_amount>")
    else:
        update.message.reply_text("You are not authorized to perform this action.")

def show_rewards(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id in ADMINS:
        rewards_text = "\n".join([f"Username: {username}, Reward: {reward}" for username, reward in REWARDS.items()])
        update.message.reply_text(rewards_text)
    else:
        update.message.reply_text("You are not authorized to perform this action.")

def main():
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("fetch_admins", fetch_admins))
    dispatcher.add_handler(CommandHandler("add_admin", add_admin))
    dispatcher.add_handler(CommandHandler("add_reward", add_reward))
    dispatcher.add_handler(CommandHandler("show_rewards", show_rewards))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()



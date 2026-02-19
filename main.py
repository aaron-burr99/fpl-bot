from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, Application, ContextTypes

import requests
from dotenv import load_dotenv
import os
from datetime import datetime, timezone, timedelta

load_dotenv()

# Replace 'YOUR_API_TOKEN' with your actual bot token from BotFather
API_TOKEN = os.getenv('API_TOKEN') 

team_ids = {'Ryan': os.getenv('RYAN'), 
            'Sean Soo': os.getenv('SEAN_SOO'), 
            'Zhong Hern': os.getenv('ZHONG_HERN'), 
            'Siyang': os.getenv('SIYANG')}

def get_last_updated_time():
    url = "https://fantasy.premierleague.com/api/leagues-classic/333/standings/?page_new_entries=1&page_standings=1&phase=1"
    headers = {
        "User-Agent": "PostmanRuntime/7.51.0",
        "Accept": "*/*",
        "Host": "fantasy.premierleague.com",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
    }
    try:
        response = requests.get(url, headers=headers)

        # Search for the specific league
        data = response.json()
        time = data['last_updated_data']
        # print(time)
        return time
    except:
        print('error in retrieving time')

async def send_message_if_got_updates(context: ContextTypes.DEFAULT_TYPE):
    last_updated_time = datetime.strptime(get_last_updated_time(), '%Y-%m-%dT%H:%M:%S%z')
    now_utc = datetime.now(timezone.utc)
    # now_utc = datetime.strptime("2026-02-13T01:37:41Z", '%Y-%m-%dT%H:%M:%S%z') #stubbed ver of time
    delta = (now_utc - last_updated_time).total_seconds()
    if delta < 10:
        try:
            print(f"time difference is {delta} secs, there must be a new update...")
            await send_message(context)
        except:
            print('got error trying to send message')
    else:
        sg_time = now_utc + timedelta(hours=8)
        print(f"at {sg_time}, time difference is {delta:.2f} secs, there is no new update...")

def get_scores(team_id):

    url = f"https://fantasy.premierleague.com/api/entry/{team_id}/"

    headers = {
        "User-Agent": "PostmanRuntime/7.51.0",
        "Accept": "*/*",
        "Host": "fantasy.premierleague.com",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
    }

    try:
        response = requests.get(url, headers=headers)

        # Search for the specific league
        data = response.json()
        classic_leagues = data['leagues']['classic']

        for league in classic_leagues:
            if league['name'] == 'Second Chance':
                total_points = league['active_phases'][0]['total']
                print(f"Total Points: {total_points}")
                return total_points
        else:
            print("League 'Second Chance' not found")
        
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except (ValueError, KeyError) as e:
        print(f"Error parsing response: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id

    # Check if the job already exists for this chat
    current_jobs = context.job_queue.get_jobs_by_name(str(chat_id))
    if current_jobs:
        await update.message.reply_text("Periodic messages are already running.")
        return

    # Add the new repeating job to the queue
    # interval=10.0 specifies the interval in seconds
    # first=0.0 means it starts immediately
    context.job_queue.run_repeating(
        send_message_if_got_updates,
        interval=10.0,
        first=0.0,
        data=chat_id,
        name=str(chat_id)
    )

    await update.message.reply_text("Who is going to treat Hai Di Lao?")
    await show_option_buttons(update, context)

async def show_option_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Check 2nd Chance Leaderboard", callback_data='button_1')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Please choose an option:', reply_markup=reply_markup)

async def button_selection_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    result = {}
    for name, team_id in team_ids.items():
        result[name] = get_scores(team_id)

    sorted_result = sorted(result.items(), key=lambda item: item[1], reverse=True)
    pretty_sorted = [f"{idx+1}. {name}: {points} pts" for idx, (name, points) in enumerate(sorted_result)]
    sorted_items_desc = "\n".join(pretty_sorted)
    await query.edit_message_text(f'{sorted_items_desc}')
    # await query.edit_message_text(f'You selected option: {query.data.split("_")[1]}')

# Function that the JobQueue will call periodically
async def send_message(context: ContextTypes.DEFAULT_TYPE):
    """Send the periodic message."""
    # The chat_id is passed via the context.job.data in this example
    print("sending message...")
    chat_id = context.job.data
    result = {}
    for name, team_id in team_ids.items():
        result[name] = get_scores(team_id)

    sorted_result = sorted(result.items(), key=lambda item: item[1], reverse=True)
    pretty_sorted = [f"{idx+1}. {name}: {points} pts" for idx, (name, points) in enumerate(sorted_result)]
    sorted_items_desc = "\n".join(pretty_sorted)
    await context.bot.send_message(chat_id=chat_id, text=f'{sorted_items_desc}')

def main():
    application = Application.builder().token(API_TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button_selection_handler, pattern='^button_'))
    application.run_polling()

if __name__ == '__main__':
    print("Bot is starting...")
    main()
    print("May our friendship last long after FPL ends...")
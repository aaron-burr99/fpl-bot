from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, Application, ContextTypes

import requests
from dotenv import load_dotenv
import os

load_dotenv()

# Replace 'YOUR_API_TOKEN' with your actual bot token from BotFather
API_TOKEN = os.getenv('API_TOKEN') 

team_ids = {'Ryan': os.getenv('RYAN'), 
            'Sean Soo': os.getenv('SEAN_SOO'), 
            'Zhong Hern': os.getenv('ZHONG_HERN'), 
            'Siyang': os.getenv('SIYANG')}
            
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

def main():
    application = Application.builder().token(API_TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button_selection_handler, pattern='^button_'))
    application.run_polling()

if __name__ == '__main__':
    print("Bot is starting...")
    main()
    print("May our friendship last long after FPL ends...")
# #!/usr/bin/python

# # This is a simple bot with schedule timer
# # https://schedule.readthedocs.io
# # -*- coding: utf-8 -*-
# """
# This Example will show you how to use register_next_step handler.

# Imports
from asyncio.windows_events import NULL
import pygsheets
from email import message
import telebot
from telebot import types
from datetime import datetime

# Pygsheet Config
service_file = r'nexlogictelegram-f7f2604d2ca9.json'
gc = pygsheets.authorize(service_file=service_file)
sheetname = 'TelegramSheet'
sh = gc.open(sheetname)
wks = sh.worksheet_by_title('Timelog')
wksnames = sh.worksheet_by_title('List')

# Telegram API Token
API_TOKEN = '5515504844:AAF5r0yxEccG1r3tKAKvlfUBNltWgqy_DNI'
bot = telebot.TeleBot(API_TOKEN)

user_dict = {}

class User:
    def __init__(self, name):
        self.timein = name
        self.timeout = None

print("Running..")

# Start
@bot.message_handler(commands=['start'])
def process_start(message):
    username = message.chat.username
    finduser = wksnames.find(username)
    nofind = int(len(finduser))
    if nofind >= 1:
        bot.reply_to(message, "Daily Time Record BOT")
    else:
        bot.reply_to(message, 'Only Intern member can use this bot')


# Help
@bot.message_handler(commands=['help'])
def process_help(message):
    username = message.chat.username
    finduser = wksnames.find(username)
    nofind = int(len(finduser))
    if nofind >= 1:
        bot.reply_to(message, "Type\n\n/timein\n/timeout")
    else:
        bot.reply_to(message, 'Only Intern member can use this bot')
    


# Timein
@bot.message_handler(commands=['timein'])   
def process_timein(message):
    username = message.chat.username
    finduser = wksnames.find(username)
    nofind = int(len(finduser))
    if nofind >= 1:
        try:
            now = datetime.now()
            date_time = now.strftime("%H:%M:%S")
            time = now.strftime("%H:%M:%S")
            date = now.strftime('%m/%d/%y')
            chat_id = message.chat.id
            timein = message.text
            user = User(timein)
            user_dict[chat_id] = user
            user.timein = date_time
            
            if timein == "/timein":
                user_first_name = str(message.chat.first_name)
                user_last_name = str(message.chat.last_name)
                full_name = user_first_name + " "+ user_last_name
                grecord = wks.get_all_records()
                num = 2
                for i in range(len(grecord)):
                    num+=1
                    if full_name == grecord[i].get("Name") and date == grecord[i].get("Date"):
                        bot.reply_to(message, f'You have already TIMED IN')
                        break
                else:
                    wks.update_value((num, 1), full_name)
                    wks.update_value((num, 2), date)
                    wks.update_value((num, 3), time)
                    # timelog = []
                    # timelog.append(str(full_name))
                    # timelog.append(str(date))
                    # timelog.append(str(time))
                    # wks.append_table(timelog)   
                    bot.reply_to(message, f'Successfully timein on {str(date_time)}')

        except Exception as e:
            bot.reply_to(message, 'Something went wrong. Please try again')
    else:
        bot.reply_to(message, 'Only Intern member can use this bot')

 
# Timeout
@bot.message_handler(commands=['timeout'])  
def process_timeout(message):
    username = message.chat.username
    finduser = wksnames.find(username)
    nofind = int(len(finduser))
    if nofind >= 1:
        try:
            now2 = datetime.now()
            date_time2 = now2.strftime("%H:%M:%S")
            time = now2.strftime("%H:%M:%S")
            timeout = message.text 
            user = User(timeout)
            user.timeout = date_time2
            user_first_name = str(message.chat.first_name)
            user_last_name = str(message.chat.last_name)
            full_name = user_first_name + " "+ user_last_name
            
            date = now2.strftime('%m/%d/%y')

            if timeout == "/timeout":
                grecord = wks.get_all_records()
                num = 1
                for i in range(len(grecord)):
                    num += 1
                    if full_name == grecord[i].get("Name") and date == grecord[i].get("Date") and grecord[i].get("Timeout")== '':
                        wks.update_value((num,4),time)
                        bot.reply_to(message, f'Successfully timeout on {str(date_time2)}')
                        break
                    elif full_name == grecord[i].get("Name") and date == grecord[i].get("Date") and grecord[i].get("Timeout")!= '':
                        bot.reply_to(message, 'You have already TIMED OUT')

        except Exception as e:
            bot.reply_to(message, 'Something went wrong. Please try again')
    else:
        bot.reply_to(message, 'Only Intern member can use this bot')


# Status
@bot.message_handler(commands=['status'])  
def process_status(message):
    username = message.chat.username
    finduser = wksnames.find(username)
    nofind = int(len(finduser))
    if nofind >= 1:
        user_first_name = str(message.chat.first_name) 
        user_last_name = str(message.chat.last_name)
        full_name = user_first_name + " "+ user_last_name
        now = datetime.now()
        date = now.strftime('%m/%d/%y')
        grecord = wks.get_all_records()
        num = 1
        for i in range(len(grecord)):
            num += 1
            if full_name == grecord[i].get("Name") and date == grecord[i].get("Date") and grecord[i].get("Timein")!= '' and grecord[i].get("Timeout")!= '':
                bot.reply_to(message, f'Date {date}\nTimein: {grecord[i].get("Timein")}\nTimeout: {grecord[i].get("Timeout")}')
                break
            elif full_name == grecord[i].get("Name") and date == grecord[i].get("Date") and grecord[i].get("Timein")!= '' and grecord[i].get("Timeout")== '':
                bot.reply_to(message, f'Date {date}\nTimein: {grecord[i].get("Timein")}\nTimeout: NONE')
                break
        else:
            bot.reply_to(message, "You haven't TIMED IN yet today")
    else:
        bot.reply_to(message, 'Only Intern member can use this bot')
# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

bot.infinity_polling()

# -*- coding: utf-8 -*-
"""
This Example will show you how to use register_next_step handler.
"""

import telebot
import pygsheets
from telebot import types
from datetime import datetime

service_file = r'nexlogictelegram-f7f2604d2ca9.json'
gc = pygsheets.authorize(service_file=service_file)
sheetname = 'TelegramSheet'

sh = gc.open(sheetname)
wks = sh.worksheet_by_title('Timelog')
wksNames = sh.worksheet_by_title('List')

API_TOKEN = '5515504844:AAF5r0yxEccG1r3tKAKvlfUBNltWgqy_DNI'

bot = telebot.TeleBot(API_TOKEN)

user_dict = {}

class User:
    def __init__(self, time1):
        self.time1 = time1
        self.tIn = None
        self.tOut = None


date1 = datetime.now()
date2 = datetime.now()

print("Starting...")
# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    msg = bot.reply_to(message, """\
Hi there, I am timelog bot.

Here are my commands \n /timein \n /timeout \n /status
""")

@bot.message_handler(commands=['timein'])
def process_in_step(message):
    timein = message.text
    if timein == "/timein":
        firstName = str(message.chat.first_name)
        LastName = str(message.chat.last_name)
        fullName = (firstName + " " + LastName)
        chat_id = message.chat.id

        #datetest="July 28, 2022"
        now = datetime.now()
        date1 = datetime.now()
        strtime = now.strftime("%H:%M:%S")
        strDate = now.strftime("%B %#d, %Y")
        date_time = now.strftime("Timeout: %m/%d/%y - %H:%M:%S")

        ListofI = wksNames.get_all_records()
        List = wks.get_all_records()
        findName = wksNames.find(fullName)
        celladd = wks.find(strDate)

        for i in range(len(ListofI)):
            if fullName == ListofI[i].get("List of Interns"):
                for j in range(len(List)):
                    if fullName == List[j].get("Intern Name") and strDate == List[j].get("Date"):
                        msg = bot.reply_to(message, "You already Timed in!")
                        break
                else:
                        timeInn = []
                        timeInn.append(str(strDate))
                        timeInn.append(str(fullName))
                        timeInn.append(str(strtime))
                        wks.append_table(timeInn)
                        msg = bot.reply_to(message, date_time + ' \n Type Timeout to log out.')

@bot.message_handler(commands=['timeout'])     
def process_out_step(message):
    timeout = message.text
    if timeout == "/timeout":
        chat_id = message.chat.id

        firstName2 = str(message.chat.first_name)
        LastName2 = str(message.chat.last_name)
        fullName2 = (firstName2 + " " + LastName2)
        now1 = datetime.now()
        date2 = datetime.now()
        strtime1 = now1.strftime("%H:%M:%S")
        strDate2 = now1.strftime("%B %#d, %Y")

        date_time1 = now1.strftime("Timeout: %m/%d/%y - %H:%M:%S")
        ListofI = wksNames.get_all_records()
        List = wks.get_all_records()

        celladd2 = wks.find(strDate2)
        for i in range(len(ListofI)):
            if fullName2 == ListofI[i].get("List of Interns"):
                num = 1
                for j in range(len(List)):
                    num += 1
                    adj2=(celladd2[0].col+1)
                    print(List[j].get("Out"))
                    if fullName2 == List[j].get("Intern Name") and strDate2 == List[j].get("Date") and List[j].get("Out") == "":
                        wks.cell((num, adj2+2)).set_value(strtime1)
                        dCell = wks.cell((num, adj2+2)).label
                        cCell = wks.cell((num, adj2+1)).label

                        formula = ("="+str(dCell)+"-"+str(cCell))
                        duration = wks.cell((num, adj2+3)).set_value(formula)
                        print(formula)
                        msg = bot.reply_to(message, date_time1)
                    elif fullName2 == List[j].get("Intern Name") and strDate2 == List[j].get("Date") and List[j].get("Out") is not None:
                        msg = bot.reply_to(message, "You are already done for today!")
                        break

@bot.message_handler(commands=['status'])     
def process_status(message):
    status = message.text
    if status== "/status":
        firstName = str(message.chat.first_name)
        LastName = str(message.chat.last_name)
        fullName = (firstName + " " + LastName)
        chat_id = message.chat.id

        now = datetime.now()
        date1 = datetime.now()
        strtime = now.strftime("%H:%M:%S")
        strDate = now.strftime("%B %#d, %Y")
        date_time = now.strftime("Timeout: %m/%d/%y - %H:%M:%S")

        ListofI = wksNames.get_all_records()
        List = wks.get_all_records()
        findName = wksNames.find(fullName)
        celladd = wks.find(strDate)

        for i in range(len(ListofI)):
            if fullName == ListofI[i].get("List of Interns"):
                for j in range(len(List)):
                    if fullName == List[j].get("Intern Name") and strDate == List[j].get("Date") and List[j].get("In") is not None and List[j].get("Out") == "" :
                        msg = bot.reply_to(message, "You already Timed in! Waiting for Time out.")
                        break
                    elif fullName == List[j].get("Intern Name") and strDate == List[j].get("Date") and List[j].get("In") is not None and List[j].get("Out") is not None :
                        msg = bot.reply_to(message, "You already Done for today!")
                        break
                    elif List[j].get("Intern Name") is None and List[j].get("Date") is None and List[j].get("In") is None and List[j].get("Out") is None:
                        msg = bot.reply_to(message, "You havent Timed in yet!")
                        break
# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=0)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

bot.infinity_polling()

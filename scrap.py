import requests
import lxml
from lxml import html
import os
import telebot
from telebot import types
from dotenv import load_dotenv
import urllib
#from urllib.parse import urlparse
headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
}

load_dotenv()
token = os.getenv('TOKEN_KEY')

bot = telebot.TeleBot(token)
# Request the page

def get_url(url):
    page = requests.get(url,headers=headers)
    tree = html.fromstring(page.content)  
    # Get element using XPath
    xp = tree.xpath('/html/body/div[3]/pre/a/@href')
    return xp


@bot.message_handler(commands = ['start'])
def start_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton('Message TahaElkarroumy', url='https://t.me/TahaElkarroumy'))
    bot.send_message(message.chat.id,"Welcome , this bot is created to help you download programming books ",reply_markup=keyboard)
    markup = types.ReplyKeyboardMarkup(row_width=2)
    for x in get_url('http://index-of.es/'):
       itembtn1 = types.KeyboardButton("/"+x) 
       markup.add(itembtn1)
    bot.send_message(message.chat.id, "Pick one :", reply_markup=markup)


@bot.message_handler(commands = get_url('http://index-of.es/'))
def get_books(message):
        page2 = requests.get('http://index-of.es'+message.text,headers=headers)
        xml = html.fromstring(page2.content)
        books = xml.xpath('/html/body/div[3]/pre/a/@href')
        bot.send_message(message.chat.id,"will take some time ")
        for b in range(1,len(books[4:]),2):
            try:   
                    filename, file_extension = os.path.splitext(books[b])
                    if file_extension == ".pdf" or file_extension == ".chm" or file_extension ==".ppt" or file_extension ==".doc":
                        bot.send_document(message.chat.id,'http://index-of.es/'+message.text+'/'+books[b])
                    else:
                        #geturl(message,books[b])
                        keyboard = telebot.types.InlineKeyboardMarkup()
                        keyboard.add(telebot.types.InlineKeyboardButton("   "+message.text+books[b], callback_data='http://index-of.es'+message.text+books[b]))
                        bot.send_message(message.chat.id,'http://index-of.es'+message.text+books[b],reply_markup=keyboard)
            except Exception as e :
                continue       
        bot.send_message(message.chat.id,"Done")   
                     
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        page2 = requests.get(call.data,headers=headers)
        xml = html.fromstring(page2.content)
        books = xml.xpath('/html/body/div[3]/pre/a/@href')
        bot.send_message(call.message.chat.id,"will take some time ")
        for b in range(1,len(books[4:]),2):
                try:   
                        filename, file_extension = os.path.splitext(books[b])
                        if file_extension == ".pdf" or file_extension == ".chm" or file_extension ==".ppt" or file_extension ==".doc":
                            bot.send_document(call.message.chat.id,call.message.text+'/'+books[b])
                        else:
                            #geturl(message,books[b])
                            keyboard = telebot.types.InlineKeyboardMarkup()
                            keyboard.add(telebot.types.InlineKeyboardButton("   "+call.message.text+books[b], callback_data= call.message.text+books[b]))
                            bot.send_message(call.message.chat.id,call.message.text+books[b],reply_markup=keyboard)
                except Exception as e :
                    continue       
        bot.send_message(call.message.chat.id,"Done")   
    except Exception as e:
        bot.send_message(call.message.chat.id,str(e))

bot.polling(none_stop=True)    

import telepot
from Chatbot import Chatbot
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton

telegram = telepot.Bot("587903621:AAGuqhADjyQdYQwmxkuNZNd7MrYYhcEKDKs")
bot = Chatbot("Masterchef")

#Recebendo Mensagem do Linguini

def recebendoMsg(msg):
    tipoMsg, tipoChat, chatID = telepot.glance(msg)
   
    frase = bot.escuta(frase = msg['text'])
    resp = bot.pensa(frase)
    if resp == 'Oie, o que voce precisa?':
        telegram.sendMessage(chatID,'Olá, o que você precisa?',
                            reply_markup=ReplyKeyboardMarkup(
                                keyboard=[
                                    [KeyboardButton(text='Receitas'), KeyboardButton(text='Aprendizado')]],
                                    one_time_keyboard=True))
    elif resp == 'lost':
        telegram.sendMessage(chatID,'Desculpe, não entendi! O que você precisa?',
                            reply_markup=ReplyKeyboardMarkup(
                                keyboard=[
                                    [KeyboardButton(text='Receitas'), KeyboardButton(text='Aprendizado')]],
                                    one_time_keyboard=True))
    else:
        telegram.sendMessage(chatID, resp)

telegram.message_loop(recebendoMsg)

    
while True:
    pass


#https://www.youtube.com/watch?v=hu0tVIPmRMc

#botões: receita, quero te ensinar  

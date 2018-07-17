﻿import telebot
from telebot import types
import gspread
import config

import re


#Подключение Google drive
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

sheet = client.open('Mykola test.xlsx').sheet1


#----------


#Настройка бота

bot = telebot.TeleBot(config.TOKEN)
print(bot.get_me())

#----------
@bot.message_handler(commands=['start'])  # Выполняется, когда пользователь нажимает на start
def send_welcome(message):

	bot.send_message(message.chat.id, 'Вас приветствует бот Leroy Merlin\nПожалуйста, введите код товара')


@bot.message_handler(content_types=["text"]) # Любой текст
def answer_message(message):

	result = sheet.get_all_records()
	send = False
	hat_written = False
	send_array = []
	send_text = ""
	
	#if re.search('[a-zA-ZА-Яа-я]', message.text):
	if re.search('\D', message.text):
		bot.send_message(message.chat.id, "Пожалуйста, номер заказа, который состоит только из цифр")
	else:
		for x  in result:
			if x.get('pyxis_order_uid') == int(message.text):
				send = True
				if x.get('provider') == 'LEROY_MERLIN':
					send_text = "\nСтатус: " + str(x.get('status')) + "\nПровайдер: " + str(x.get('provider'))  + "\nВнешний ключ: " + str(x.get('external_id')) + "\nПолучите доставку в одном из магазинов\n"
				


				elif x.get('provider') == 'AVITEK_INVEST':
					send_text = send_text + "\nСтатус: " + str(x.get('status')) + "\nПровайдер: " + str(x.get('provider'))  + "\nВнешний ключ: " + str(x.get('external_id')) + "\nОжидайте доставку домой\n"



				elif x.get('provider') == 'NOVA_POSHTA':			
					if hat_written == False:
						send_array.append("Статус: " + str(x.get('status')) + "\nПровайдер: " + str(x.get('provider')) + "\n")
						hat_written = True
					if x.get('status_2') == 1:
						send_array.append("\nВнешний ключ " + ": " + str(x.get('external_id')) + "\nСтатус Новой Почты" + ": " + "Нова пошта очікує надходження від відправника\n")
					elif x.get('status_2') == 2:
						send_array.append("\nВнешний ключ " + ": " + str(x.get('external_id')) + "\nСтатус Новой Почты" + ": " + "Видалено\n")


					'''if x.get('status_2') == 1:
						send_text = send_text + "\nСтатус: " + str(x.get('status')) + "\nПровайдер: " + str(x.get('provider'))  + "\nВнешний ключ: " + str(x.get('external_id')) + "\nСтатус Новой Почты: " + "Нова пошта очікує надходження від відправника\n"
					elif x.get('status_2') == 2:
						send_text = send_text + "\nСтатус: " + str(x.get('status')) + "\nПровайдер: " + str(x.get('provider'))  + "\nВнешний ключ: " + str(x.get('external_id')) + "\nСтатус Новой Почты: " + "Видалено\n"
					elif x.get('status_2') == 3:
						send_text = send_text + "\nСтатус: " + str(x.get('status')) + "\nПровайдер: " + str(x.get('provider'))  + "\nВнешний ключ: " + str(x.get('external_id')) + "\nСтатус Новой Почты: " + "Номер не знайдено\n"
					elif x.get('status_2') == 4:
						send_text = send_text + "\nСтатус: " + str(x.get('status')) + "\nПровайдер: " + str(x.get('provider'))  + "\nВнешний ключ: " + str(x.get('external_id')) + "\nСтатус Новой Почты: " + "Відправлення у місті ХХXХ. (Статус для межобластных отправлений)\n"
					elif x.get('status_2') == 5:
						send_text = send_text + "\nСтатус: " + str(x.get('status')) + "\nПровайдер: " + str(x.get('provider'))  + "\nВнешний ключ: " + str(x.get('external_id')) + "\nСтатус Новой Почты: " + "Відправлення прямує до міста YYYY\n"
					elif x.get('status_2') == 6:
						send_text = send_text + "\nСтатус: " + str(x.get('status')) + "\nПровайдер: " + str(x.get('provider'))  + "\nВнешний ключ: " + str(x.get('external_id')) + "\nСтатус Новой Почты: " + "Відправлення у місті YYYY, орієнтовна доставка до ВІДДІЛЕННЯ-XXX dd-mm. Очікуйте додаткове повідомлення про прибуття\n"
					elif x.get('status_2') == 7 or x.get('status_2') == 8:
						send_text = send_text + "\nСтатус: " + str(x.get('status')) + "\nПровайдер: " + str(x.get('provider'))  + "\nВнешний ключ: " + str(x.get('external_id')) + "\nСтатус Новой Почты: " + "Прибув на відділення\n"
					elif x.get('status_2') == 9:
						send_text = send_text + "\nСтатус: " + str(x.get('status')) + "\nПровайдер: " + str(x.get('provider'))  + "\nВнешний ключ: " + str(x.get('external_id')) + "\nСтатус Новой Почты: " + "Відправлення отримано\n"
					elif x.get('status_2') == 10:
						send_text = send_text + "\nСтатус: " + str(x.get('status')) + "\nПровайдер: " + str(x.get('provider'))  + "\nВнешний ключ: " + str(x.get('external_id')) + "\nСтатус Новой Почты: " + "Відправлення отримано %DateReceived%. Протягом доби ви одержите SMS-повідомлення про надходження грошового переказу та зможете отримати його в касі відділення «Нова пошта»\n"
					elif x.get('status_2') == 11:
						send_text = send_text + "\nСтатус: " + str(x.get('status')) + "\nПровайдер: " + str(x.get('provider'))  + "\nВнешний ключ: " + str(x.get('external_id')) + "\nСтатус Новой Почты: " + "Відправлення отримано %DateReceived%. Грошовий переказ видано одержувачу\n"
					elif x.get('status_2') == 14:
						send_text = send_text + "\nСтатус: " + str(x.get('status')) + "\nПровайдер: " + str(x.get('provider'))  + "\nВнешний ключ: " + str(x.get('external_id')) + "\nСтатус Новой Почты: " + "Відправлення передано до огляду отримувачу\n"
					elif x.get('status_2') == 101:
						send_text = send_text + "\nСтатус: " + str(x.get('status')) + "\nПровайдер: " + str(x.get('provider'))  + "\nВнешний ключ: " + str(x.get('external_id')) + "\nСтатус Новой Почты: " + "На шляху до одержувача\n"
					elif x.get('status_2') == 102 or x.get('status_2') == 103 or x.get('status_2') == 108:
						send_text = send_text + "\nСтатус: " + str(x.get('status')) + "\nПровайдер: " + str(x.get('provider'))  + "\nВнешний ключ: " + str(x.get('external_id')) + "\nСтатус Новой Почты: " + "Відмова одержувача\n"
					elif x.get('status_2') == 104:
						send_text = send_text + "\nСтатус: " + str(x.get('status')) + "\nПровайдер: " + str(x.get('provider'))  + "\nВнешний ключ: " + str(x.get('external_id')) + "\nСтатус Новой Почты: " + "Змінено адресу\n"
					elif x.get('status_2') == 105:
						send_text = send_text + "\nСтатус: " + str(x.get('status')) + "\nПровайдер: " + str(x.get('provider'))  + "\nВнешний ключ: " + str(x.get('external_id')) + "\nСтатус Новой Почты: " + "Припинено зберігання\n"
					elif x.get('status_2') == 106:
						send_text = send_text + "\nСтатус: " + str(x.get('status')) + "\nПровайдер: " + str(x.get('provider'))  + "\nВнешний ключ: " + str(x.get('external_id')) + "\nСтатус Новой Почты: " + "Одержано і є ТТН грошовий переказ\n"
					elif x.get('status_2') == 107:
						send_text = send_text + "\nСтатус: " + str(x.get('status')) + "\nПровайдер: " + str(x.get('provider'))  + "\nВнешний ключ: " + str(x.get('external_id')) + "\nСтатус Новой Почты: " + "Нараховується плата за зберігання\n"
					else:
						send_text = send_text + "\nСтатус: " + str(x.get('status')) + "\nПровайдер: " + str(x.get('provider'))  + "\nВнешний ключ: " + str(x.get('external_id')) + "\nСтатус Новой Почты: " + "-\n"'''
					
		if send == False:
			send_text = "К сожалению, такого кода товара нет"



	send_message(message.chat.id, send_text, send_array)

			



def send_message(id, text, array): 	
	text = ""
	seen = []
	result = []
	for item in array:
    		if item not in seen:
     			seen.append(item)
     			result.append(item)

	text = text + result[0]

	turn = 0

	for x in result:
		text = text + str(turn ) + ")" + str(x)
	
		
	bot.send_message(id, text)




if __name__ == '__main__':
    	bot.polling(none_stop=True)
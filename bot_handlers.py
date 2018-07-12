import telebot
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
def repeat_all_messages(message):

	result = sheet.get_all_records()
	send = False 
	
	if re.search('[a-zA-ZА-Яа-я]', message.text):
		bot.send_message(message.chat.id, "Пожалуйста, введите код, который состоит только из цифр")
	else:
		for x  in result:
			if x.get('pyxis_order_uid') == int(message.text):
				send = True
				if x.get('provider') == 'LEROY_MERLIN':
					bot.send_message(message.chat.id, "Статус: " + str(x.get('status') + "\nПровайдер: " + str(x.get('provider'))  + "\nВнешний ключ: " + str(x.get('external_id')) + "\nПолучите доставку в одном из магазинов"))
				elif x.get('provider') == 'AVITEK_INVEST':
					bot.send_message(message.chat.id, "Статус: " + str(x.get('status') + "\nПровайдер: " + str(x.get('provider'))  + "\nВнешний ключ: " + str(x.get('external_id')) + "\nОжидайте доставку домой"))
				elif x.get('provider') == 'NOVA_POSHTA':
					if x.get('status_2') == 1:
						bot.send_message(message.chat.id, "Статус: " + str(x.get('status') + "\nПровайдер: " + str(x.get('provider'))  + "\nВнешний ключ: " + str(x.get('external_id')) + "\nСтатус Новой Почты: " + "Нова пошта очікує надходження від відправника"))
					elif x.get('status_2') == 2:
						bot.send_message(message.chat.id, "Статус: " + str(x.get('status') + "\nПровайдер: " + str(x.get('provider'))  + "\nВнешний ключ: " + str(x.get('external_id')) + "\nСтатус Новой Почты: " + "Видалено"))
					elif x.get('status_2') == 3:
						bot.send_message(message.chat.id, "Статус: " + str(x.get('status') + "\nПровайдер: " + str(x.get('provider'))  + "\nВнешний ключ: " + str(x.get('external_id')) + "\nСтатус Новой Почты: " + "Номер не знайдено"))
					elif x.get('status_2') == 4:
						bot.send_message(message.chat.id, "Статус: " + str(x.get('status') + "\nПровайдер: " + str(x.get('provider'))  + "\nВнешний ключ: " + str(x.get('external_id')) + "\nСтатус Новой Почты: " + "Відправлення у місті ХХXХ. (Статус для межобластных отправлений)"))
					elif x.get('status_2') == 5:
						bot.send_message(message.chat.id, "Статус: " + str(x.get('status') + "\nПровайдер: " + str(x.get('provider'))  + "\nВнешний ключ: " + str(x.get('external_id')) + "\nСтатус Новой Почты: " + "Відправлення прямує до міста YYYY"))
					elif x.get('status_2') == 6:
						bot.send_message(message.chat.id, "Статус: " + str(x.get('status') + "\nПровайдер: " + str(x.get('provider'))  + "\nВнешний ключ: " + str(x.get('external_id')) + "\nСтатус Новой Почты: " + "Відправлення у місті YYYY, орієнтовна доставка до ВІДДІЛЕННЯ-XXX dd-mm. Очікуйте додаткове повідомлення про прибуття."))
					elif x.get('status_2') == 7 or x.get('status_2') == 8:
						bot.send_message(message.chat.id, "Статус: " + str(x.get('status') + "\nПровайдер: " + str(x.get('provider'))  + "\nВнешний ключ: " + str(x.get('external_id')) + "\nСтатус Новой Почты: " + "Прибув на відділення"))
					elif x.get('status_2') == 9:
						bot.send_message(message.chat.id, "Статус: " + str(x.get('status') + "\nПровайдер: " + str(x.get('provider'))  + "\nВнешний ключ: " + str(x.get('external_id')) + "\nСтатус Новой Почты: " + "Відправлення отримано"))
					elif x.get('status_2') == 10:
						bot.send_message(message.chat.id, "Статус: " + str(x.get('status') + "\nПровайдер: " + str(x.get('provider'))  + "\nВнешний ключ: " + str(x.get('external_id')) + "\nСтатус Новой Почты: " + "Відправлення отримано %DateReceived%. Протягом доби ви одержите SMS-повідомлення про надходження грошового переказу та зможете отримати його в касі відділення «Нова пошта»."))
					elif x.get('status_2') == 11:
						bot.send_message(message.chat.id, "Статус: " + str(x.get('status') + "\nПровайдер: " + str(x.get('provider'))  + "\nВнешний ключ: " + str(x.get('external_id')) + "\nСтатус Новой Почты: " + "Відправлення отримано %DateReceived%. Грошовий переказ видано одержувачу."))
					elif x.get('status_2') == 14:
						bot.send_message(message.chat.id, "Статус: " + str(x.get('status') + "\nПровайдер: " + str(x.get('provider'))  + "\nВнешний ключ: " + str(x.get('external_id')) + "\nСтатус Новой Почты: " + "Відправлення передано до огляду отримувачу"))
					elif x.get('status_2') == 101:
						bot.send_message(message.chat.id, "Статус: " + str(x.get('status') + "\nПровайдер: " + str(x.get('provider'))  + "\nВнешний ключ: " + str(x.get('external_id')) + "\nСтатус Новой Почты: " + "На шляху до одержувача"))
					elif x.get('status_2') == 102 or x.get('status_2') == 103 or x.get('status_2') == 108:
						bot.send_message(message.chat.id, "Статус: " + str(x.get('status') + "\nПровайдер: " + str(x.get('provider'))  + "\nВнешний ключ: " + str(x.get('external_id')) + "\nСтатус Новой Почты: " + "Відмова одержувача"))	
					elif x.get('status_2') == 104:
						bot.send_message(message.chat.id, "Статус: " + str(x.get('status') + "\nПровайдер: " + str(x.get('provider'))  + "\nВнешний ключ: " + str(x.get('external_id')) + "\nСтатус Новой Почты: " + "Змінено адресу"))
					elif x.get('status_2') == 105:
						bot.send_message(message.chat.id, "Статус: " + str(x.get('status') + "\nПровайдер: " + str(x.get('provider'))  + "\nВнешний ключ: " + str(x.get('external_id')) + "\nСтатус Новой Почты: " + "Припинено зберігання"))
					elif x.get('status_2') == 106:
						bot.send_message(message.chat.id, "Статус: " + str(x.get('status') + "\nПровайдер: " + str(x.get('provider'))  + "\nВнешний ключ: " + str(x.get('external_id')) + "\nСтатус Новой Почты: " + "Одержано і є ТТН грошовий переказ"))
					elif x.get('status_2') == 107:
						bot.send_message(message.chat.id, "Статус: " + str(x.get('status') + "\nПровайдер: " + str(x.get('provider'))  + "\nВнешний ключ: " + str(x.get('external_id')) + "\nСтатус Новой Почты: " + "Нараховується плата за зберігання"))
					else:
						bot.send_message(message.chat.id, "Статус: " + str(x.get('status') + "\nПровайдер: " + str(x.get('provider'))  + "\nВнешний ключ: " + str(x.get('external_id')) + "\nСтатус Новой Почты: " + "-"))
					
		if send == False:
			bot.send_message(message.chat.id, "К сожалению, такого кода товара нет")

			








if __name__ == '__main__':
    	bot.polling(none_stop=True)
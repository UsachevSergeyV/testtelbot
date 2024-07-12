import telebot
import time
f = open("token", 'r')
bot = telebot.TeleBot(f.readline())
f.close()

#наборы стикеров
sticker_set_name = "TidyTieTom"
# Получаем набор стикеров
sticker_set = bot.get_sticker_set(sticker_set_name)
sticker = sticker_set.stickers[19]
sticker_id = sticker.file_id
print(sticker_id)


#Делаем набор кнопок
keyboard = telebot.types.InlineKeyboardMarkup()
button1 = telebot.types.InlineKeyboardButton("YES", callback_data="yes_callback_func")
button2 = telebot.types.InlineKeyboardButton("NO", callback_data="no_callback_func")
button3 = telebot.types.InlineKeyboardButton("DISABLE", callback_data="NO_DIS" )
keyboard.add(button1, button2,button3)

#Делаем реплай кнопки
keyboardInline = telebot.types.ReplyKeyboardMarkup()
button3 = telebot.types.InlineKeyboardButton("Fitst button")
button4 = telebot.types.InlineKeyboardButton("Second button")
keyboardInline.add(button3, button4)



#Обработчик ответа на сообщение с типом text
@bot.message_handler(content_types=['text'])
def functionHandlerText(message):
    if message.text=="Вопрос":
        bot.send_message(chat_id=message.from_user.id,text="Ответ")
    if message.text.isnumeric():
        if message.text=='111':
            #Кнопки по нажати на которые будет выполнятся callback функция соответствующая этой кнопке
            bot.send_message(chat_id=message.from_user.id,text="Получаем инлайн кнопки к сообщению",reply_markup=keyboard)

        if message.text=='222':
            #Кнопки по нажатию будут кидать в ответ в чат какое то сообщение написанное на кнопке
            bot.send_message(chat_id=message.from_user.id,text="Получаем реплай кнопке к сообщению",reply_markup=keyboardInline)


#обработчик ответа на сообщеине типа document
@bot.message_handler(content_types=['document'])
def functionHandlerText2(message):
    if str(message.caption).startswith("Вопрос"):
        bot.send_message(chat_id=message.from_user.id,text="Ответ2")

#Колбэк обработчики которые будут обрабатывать соответствующие сигналы, отправляем в виде ответа на сообщение к которому было сгенерирована панель с кнопкаи
@bot.callback_query_handler(func=lambda call: call.data == 'yes_callback_func')
def yes_callback_def(call):
    bot.send_message(call.message.chat.id, 'Ответ на кнопку yes', reply_to_message_id=call.message.id-1)
@bot.callback_query_handler(func=lambda call: call.data == 'no_callback_func')
def yes_callback_def(call):
    #убиваем кнопки
    bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup=None)
    #меняем текст
    bot.edit_message_text(chat_id=call.message.chat.id,message_id= call.message.id, text="Вычисляем вычисления 🔄 ⚙️ ⌛️  ✅ ❌")
    #шлем стикер
    messageSticrer = bot.send_sticker(chat_id=call.message.chat.id, sticker=sticker_id)

    # Удаляем сообщение вообще но через 5 секунд - при этом поток умирает, так же удаляем стикер
    time.sleep(5)
    bot.delete_message(chat_id=call.message.chat.id, message_id=messageSticrer.id)
    bot.delete_message(chat_id=call.message.chat.id,message_id= call.message.id)
    # Отправляем ответ
    bot.send_message(call.message.chat.id, 'Ответ на кнопку no', reply_to_message_id=call.message.id-1)
bot.polling(none_stop=True, interval=0)





